# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ex2_producto_vender.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProductoVender(object):
    def setupUi(self, ProductoVender):
        ProductoVender.setObjectName("ProductoVender")
        ProductoVender.resize(320, 120)
        ProductoVender.setMinimumSize(QtCore.QSize(320, 120))
        ProductoVender.setMaximumSize(QtCore.QSize(320, 120))
        self.gridLayout = QtWidgets.QGridLayout(ProductoVender)
        self.gridLayout.setObjectName("gridLayout")
        self.lay_frm_principal = QtWidgets.QFormLayout()
        self.lay_frm_principal.setHorizontalSpacing(20)
        self.lay_frm_principal.setObjectName("lay_frm_principal")
        self.lbl_codigo = QtWidgets.QLabel(ProductoVender)
        self.lbl_codigo.setObjectName("lbl_codigo")
        self.lay_frm_principal.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_codigo)
        self.txt_codigo = QtWidgets.QLineEdit(ProductoVender)
        self.txt_codigo.setObjectName("txt_codigo")
        self.lay_frm_principal.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_codigo)
        self.lbl_cantidad = QtWidgets.QLabel(ProductoVender)
        self.lbl_cantidad.setObjectName("lbl_cantidad")
        self.lay_frm_principal.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_cantidad)
        self.spx_cantidad = QtWidgets.QSpinBox(ProductoVender)
        self.spx_cantidad.setObjectName("spx_cantidad")
        self.lay_frm_principal.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spx_cantidad)
        self.btn_vender = QtWidgets.QPushButton(ProductoVender)
        self.btn_vender.setObjectName("btn_vender")
        self.lay_frm_principal.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.btn_vender)
        self.gridLayout.addLayout(self.lay_frm_principal, 0, 0, 1, 1)

        self.retranslateUi(ProductoVender)
        QtCore.QMetaObject.connectSlotsByName(ProductoVender)

    def retranslateUi(self, ProductoVender):
        _translate = QtCore.QCoreApplication.translate
        ProductoVender.setWindowTitle(_translate("ProductoVender", "Vender Producto"))
        self.lbl_codigo.setText(_translate("ProductoVender", "Codigo: "))
        self.lbl_cantidad.setText(_translate("ProductoVender", "Cantidad: "))
        self.btn_vender.setText(_translate("ProductoVender", "vender"))
