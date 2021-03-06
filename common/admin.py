from django.contrib import admin
from django.forms import BaseInlineFormSet

from blockchain.jsonrpc.ethereum import EthereumAPI
from common import Owner, Sensor, SensorData, Transaction

__author__ = 'nikolas'


class SensorDataInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        qs = super(SensorDataInlineFormSet, self).get_queryset()
        return qs[:25]


class SensorDataInline(admin.TabularInline):
    model = SensorData
    ordering = ["-timestamp"]
    max_num = 1
    fields = ['timestamp', 'value']
    readonly_fields = ['timestamp', 'value']
    can_delete = False
    formset = SensorDataInlineFormSet


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    def compile_code(self, request, qs):
        for owner in qs:
            owner.compile_contract()

    def deploy_contract(self, request, qs):
        for owner in qs:
            owner.deploy_contract()

    compile_code.short_description = "Compile code to lll"
    actions = [compile_code, deploy_contract]
    list_display = ['name', 'block_chain_account', 'blockchain_balance', 'contract_balance']


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", 'blockchain_value', 'data_dt_start', 'data_dt_end']
    inlines = [SensorDataInline]

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'timestamp', 'value']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['hash_id', 'cost', 'dt_start', 'dt_end', 'status']