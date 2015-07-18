# -*- coding: utf-8 -*-
'''
File Name: server.py
Author: JackeyGao
mail: junqi.gao@shuyun.com
Created Time: 五  7/17 22:25:40 2015
'''
import tornado.ioloop
import tornado.web
import shutil
import commands
import os
import uuid


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static") 
}
 
class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload.html", message=u"请先上传jpg文件", color="green", content=None)
 
    def post(self):
        upload_path=os.path.join(os.path.dirname(__file__),'files')  #文件的暂存路径
        if not self.request.files.has_key('file'):
            self.render("upload.html", message=u"没有上传jpg文件哦", 
                    color="red", content=None)
            return

        file_metas=self.request.files['file']    #提取表单中‘name’为‘file’的文件元数据
        file_uuid = uuid.uuid1().hex

        for meta in file_metas:
            filename=file_uuid + '_' + meta['filename']
            filepath=os.path.join(upload_path,filename)
            with open(filepath,'wb') as up:      #有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
        
        status, output = commands.getstatusoutput("jp2a --background=light --width=65 %s" % filepath)

        if status <> 0:
            self.render("upload.html", content=output, message="转换出错", color="red")
            return

        self.render("upload.html", content=output, message="转换成功", color="green")
 
app=tornado.web.Application([
    (r'^/$',UploadFileHandler),
], **settings)
 
if __name__ == '__main__':
    app.listen(3000)
    tornado.ioloop.IOLoop.instance().start()
