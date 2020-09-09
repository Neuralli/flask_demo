# coding = utf-8

from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 创建flask 的应用对象
"""
development:    开发环境
production:     生产环境
"""
app = create_app("product")

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()

