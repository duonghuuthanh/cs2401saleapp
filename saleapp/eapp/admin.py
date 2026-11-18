from flask_admin import Admin, BaseView, expose, AdminIndexView
from urllib3 import request
from wtforms.fields.numeric import FloatField
from eapp import app, db, dao
from flask_admin.contrib.sqla import ModelView
from eapp.models import Category, Product, UserRoleEnum
from flask_login import logout_user, current_user
from flask import redirect
from datetime import datetime
from flask import request

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.count_products_by_cate())

admin = Admin(app=app, name='eCommerce Admin', index_view=MyAdminIndex())

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
        stats_by_products = dao.stats_revenue_by_products(kw=request.args.get('kw'))

        y = request.args.get('year')
        if not y:
            y = datetime.now().year
        stats_by_time = dao.stats_revenue_by_time(year=y, time=request.args.get('time', 'month'))
        return self.render('admin/stats.html', stats_by_products=stats_by_products, stats_by_time=stats_by_time)


class LogoutView(BaseAdminAuthenticated):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

admin.add_view(AdminAuthenticated(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))