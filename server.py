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
        file_metas = self.request.files.get("file", None)
        if file_metas is None:
            self.render("upload.html", message=u"没有上传jpg文件哦", 
                    color="red", content=None)
            return

        file_uuid = uuid.uuid1().hex

        for meta in file_metas:
            filepath=os.path.join(upload_path, file_uuid + '_' + meta['filename'])
            with open(filepath,'wb') as up:
                up.write(meta['body'])
        
        code, out = commands.getstatusoutput("jp2a --background=light --width=65 %s" \
                % filepath.encode("utf-8"))

        if code <> 0:
            self.render("upload.html", content=out, message="转换出错, ErrCode:%d"\
                    % status , color="red")
            return

        self.render("upload.html", content=out, message="转换成功", color="green")
 
app=tornado.web.Application([
    (r'^/$',UploadFileHandler),
], **settings)
 
if __name__ == '__main__':
    app.listen(3000)
    tornado.ioloop.IOLoop.instance().start()
