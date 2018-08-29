from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from baseapp.decorators import admin_required
from itemmanager.models import *
from itemmanager.forms import SaleItemForm, BaseSaleItemFormSet

from collections import defaultdict
import math


class SaleListView(TemplateView):
    model = Sale
    template_name = 'sale_list.html'

    def get_context_data(self, *args, **kwargs):
        pagination = kwargs.get('page')
        request = kwargs.get('request')
        try:
            pagination = int(pagination) - 1
        except ValueError:
            pagination = 0
        pagination = pagination if pagination > 0 else 0
        sales_per_page = 10
        admin = request.session['ts_user']['is_admin']
        sales = Sale.objects.order_by('-date_created')
        if not admin:
            sales = sales.filter(user_on_duty=request.user)
        max_pagination = math.ceil(sales.count() / sales_per_page)
        min_sale_index = pagination*sales_per_page
        context = {
            'sales': sales[min_sale_index:min_sale_index+sales_per_page],
            'paginations': range(1, max_pagination+1),
            'pagination': pagination + 1,
            'min_sale_index': min_sale_index,
            'active_tab': 'sale'
        }
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        pagination = request.GET.get('p', '') or 1
        context = self.get_context_data(page=pagination, request=request)
        return render(request, self.template_name, context)


class SaleNewView(TemplateView):
    template_name = 'sale_new.html'
    SaleItemFormSet = formset_factory(
            SaleItemForm, formset=BaseSaleItemFormSet)

    def get_context_data(self, *args, **kwargs):
        context = {
            'saleitem_formset': kwargs.get('formset'),
            'active_tab': 'sale'
        }
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        saleitem_formset = self.SaleItemFormSet()

        context = self.get_context_data(formset=saleitem_formset)
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        saleitem_formset = self.SaleItemFormSet(request.POST)
        saleitem_formset.clean()
        if saleitem_formset.is_valid():
            # Create sale
            sale = Sale(user_on_duty=request.user)
            sale.save()

            # Make unique
            sales = defaultdict(int)
            for saleitem_form in saleitem_formset:
                item_pk = saleitem_form.cleaned_data.get('item')
                quantity = saleitem_form.cleaned_data.get('quantity')
                item = Item.objects.get(pk=item_pk)
                sales[item] += quantity

            # Save all saleitems
            for item, quantity in sales.items():
                price = item.item_price*quantity
                sale_item = SaleItem(sale=sale, item=item, sale_amount=quantity, sale_price=price)
                sale_item.save()
            
            return redirect('sale_detail', pk=sale.pk)
        else:
            context = self.get_context_data(formset=saleitem_formset)
            return render(request, self.template_name, context)


class SaleDetailView(TemplateView):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return redirect('pricelist')


class SaleDeleteView(TemplateView):
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        pass
