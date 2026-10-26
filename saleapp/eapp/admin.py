from flask_admin import Admin, BaseView, expose
from wtforms.fields.numeric import FloatField

from eapp import app, db
from flask_admin.contrib.sqla import ModelView
from eapp.models import Category, Product, UserRoleEnum
from flask_login import logout_user, current_user
from flask import redirect


admin = Admin(app=app, name='eCommerce Admin')

class AdminAuthenticated(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class ProductView(AdminAuthenticated):
    column_list = ['id', 'name', 'price', 'active']
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['id', 'name', 'price']
    edit_modal = True
    column_editable_list = ['name']
    can_view_details = True
    details_modal = True
    form_overrides = {
        'price': FloatField
    }


class BaseAdminAuthenticated(BaseView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class StatsView(BaseAdminAuthenticated):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(BaseAdminAuthenticated):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

admin.add_view(AdminAuthenticated(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))