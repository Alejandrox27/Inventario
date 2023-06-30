from .modelos.inventario import Inventario
from .modelos.producto import Producto
from .modelos.venta import Venta
import datetime
import os                
import pickle
import markdown

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidgetItem, QInputDialog
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from .GUI.ex2_gestor_inventario import Ui_GestorInventario
from .GUI.ex2_producto_crear import Ui_ProductoCrear
from .GUI.ex2_producto_buscar import Ui_ProductoBuscar
from .GUI.ex2_producto_vender import Ui_ProductoVender
from .GUI.ex2_producto_cambiar_disponibilidad import Ui_ProductoCambiarDisponibilidad
from .GUI.ex2_reporte_top_5 import Ui_Reporte_top5
from .GUI.ex2_reporte_ventas_rango_fecha import Ui_ReporteVentasRangoFecha
from .GUI.ex2_reporte_listado_productos import Ui_Reporte_listado_productos
from .GUI.ex2_producto_agregar_unidades import Ui_ProductoAgregarUnidades

class GestorInventarioAplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.inventario = Inventario()
        self.inicializarGui()
        
    
    def closeEvent(self, event):
        if len(self.inventario.productos) or len(self.inventario.ventas):
            self.guardar_datos_gui(self.inventario)
            self.close()
        else:
            self.close()
    
    def inicializarGui(self):
        self.ui = Ui_GestorInventario()
        self.ui.setupUi(self)
        
        
        
        self.ui.mni_producto_registrar.triggered.connect(self.registrar_producto)
        self.ui.mni_producto_buscar.triggered.connect(self.buscar_producto)
        self.ui.mni_producto_vender.triggered.connect(self.vender_producto)
        self.ui.mni_producto_cambiar_disponibilidad.triggered.connect(self.cambiar_disponibilidad_producto)
        self.ui.mni_acerca_de.triggered.connect(self.acerca_de)
        self.ui.mni_reporte_productos_mas_vendidos.triggered.connect(self.reporte_productos_mas_vendidos)
        self.ui.mni_reporte_productos_menos_vendidos.triggered.connect(self.reporte_productos_menos_vendidos)
        self.ui.mni_reporte_rango_fechas.triggered.connect(self.reporte_rango_fechas)
        self.ui.mni_listado_de_productos.triggered.connect(self.reporte_listado_productos)
        self.ui.mni_producto_agregar_unidades.triggered.connect(self.producto_agregar_unidades)
        self.ui.mni_salir.triggered.connect(self.close)
        
        self.show()
        
        if os.path.isfile('inventario/inventario.pickle'):
            resultado = self.cargar_inventario_gui()
            
            if resultado:
                self.inventario.productos = resultado.productos
                self.inventario.ventas = resultado.ventas
        
    
    def acerca_de(self):
        self.mensaje = QMessageBox(self)
        self.mensaje.setWindowTitle('Mensaje')
        self.mensaje.setText('Creador - Alejandro\n'
                             'version - 2.0')
        self.mensaje.setIcon(QMessageBox.Information)
        self.mensaje.exec_()
        
    def registrar_producto(self):
        gui = ProductoCrear(self.inventario)
        self.ui.mdi_principal.addSubWindow(gui)
        gui.show()
        
    def vender_producto(self):
        gui = ProductoVender(self.inventario)
        self.ui.mdi_principal.addSubWindow(gui)
        gui.show()
        
    def buscar_producto(self):
        gui = ProductoBuscar(self.inventario)
        self.ui.mdi_principal.addSubWindow(gui)
        gui.show()
        
    def cambiar_disponibilidad_producto(self):
        gui = ProductoCambiarDisponibilidad(self.inventario)
        self.ui.mdi_principal.addSubWindow(gui)
        gui.show()
        
    def reporte_rango_fechas(self):
        gui = ReporteRangoFecha(self.inventario)
        self.ui.mdi_principal.addSubWindow(gui)
        gui.show()
    
    def reporte_productos_mas_vendidos(self):
        gui = ReporteProductosMasVendidos(self.inventario)
        self.ui.mdi_principal.addSubWindow(gui)
        gui.show()
        
    def reporte_productos_menos_vendidos(self):
        gui = ReporteProductosMenosVendidos(self.inventario)
        self.ui.mdi_principal.addSubWindow(gui)
        gui.show()
        
    def reporte_listado_productos(self):
        gui = ReporteListadoProductos(self.inventario)
        self.ui.mdi_principal.addSubWindow(gui)
        gui.show()
        
    def producto_agregar_unidades(self):
        gui = ProductoAgregarUnidades(self.inventario)
        self.ui.mdi_principal.addSubWindow(gui)
        gui.show()
        
    def cargar_inventario_gui(self):
        confirmacion = QMessageBox()
        texto = '¿Quiere cargar los datos de inventario?'
        confirmacion.setText(texto)
        confirmacion.setIcon(QMessageBox.Question)
        confirmacion.setWindowTitle('Cargar')
        confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        boton_yes = confirmacion.button(QMessageBox.Yes)
        
        confirmacion.exec_()
        
        if confirmacion.clickedButton() == boton_yes:
            with open('inventario/inventario.pickle', 'rb') as f:
                inventario = pickle.load(f)
                return inventario
        return None
    
    def guardar_datos_gui(self, inventario):
        confirmacion = QMessageBox()
        texto = '¿Quiere guardar los datos de inventario?'
        confirmacion.setText(texto)
        confirmacion.setIcon(QMessageBox.Question)
        confirmacion.setWindowTitle('Guardar')
        confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        boton_yes = confirmacion.button(QMessageBox.Yes)
        
        confirmacion.exec_()
        
        if confirmacion.clickedButton() == boton_yes:
            #guardar los datos en el archivo inventario.pickle
            with open('inventario/inventario.pickle','wb') as f:
                pickle.dump(inventario,f)
            return True
        else:
            return False
        
class ProductoCrear(QWidget):
    def __init__(self, inventario):
        super().__init__()
        
        self.inventario = inventario
        
        self.inicializarGui()
        
    def inicializarGui(self):
        
        self.ui = Ui_ProductoCrear()
        self.ui.setupUi(self)
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setWindowTitle('mensaje')
        
        self.ui.btn_registrar.clicked.connect(self.producto_crear)
        self.ui.txt_codigo.setValidator(QIntValidator(1, 1000000, self))
        self.ui.txt_precio.setValidator(QDoubleValidator(1, 10000000, 2))
        self.ui.spx_cantidad.setMinimum(1)
        
    def producto_crear(self):
        codigo = self.ui.txt_codigo.text()
        
        if len(codigo) == 0:
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.setText('El campo codigo es obligatorio')
            self.mensaje.exec_()
            return
        else:
            codigo = int(codigo)
        
        if self.inventario.buscar_producto(codigo):
            producto = self.inventario.buscar_producto(codigo)
            self.mensaje.setIcon(QMessageBox.Question)
            self.mensaje.setText(markdown.markdown(f'Ya existe un producto con el codigo especificado\nDesea agregar más cantidad a este producto?:\n **{producto.nombre}**'))
            self.mensaje.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            boton_yes = self.mensaje.button(QMessageBox.Yes)
            self.mensaje.exec_()
            
            if self.mensaje.clickedButton() == boton_yes:
                unidades, ok = QInputDialog.getInt(self, 'Unidades a agregar','Escriba el numero de unidades a agregar', 0, 1 , 99)
        
                if ok:
                    producto.cantidad += int(unidades)
                    mensaje = QMessageBox(self)
                    mensaje.setWindowTitle('mensaje')
                    mensaje.setIcon(QMessageBox.Information)
                    mensaje.setText(markdown.markdown(f'Se agregaron las **{unidades} unidades** al producto **{producto.nombre}**'))
                    mensaje.exec_()
                    return
                else:
                    return
            else:
                return
        
        nombre = self.ui.txt_nombre.text().strip()
        
        if len(nombre) == 0:
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.setText('El campo nombre es obligatorio')
            self.mensaje.exec_()
            return
        
        precio = self.ui.txt_precio.text()
        
        if len(precio) == 0:
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.setText('El campo precio es obligatorio')
            self.mensaje.exec_()
            return
        else:
            try:
                precio = float(precio)
            except ValueError as e:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText('Hubo un error en el campo precio,\n pon "." para marcar los decimales')
                self.mensaje.exec_()
                return
        
        cantidad = int(self.ui.spx_cantidad.value())
        
        disponible = self.ui.chk_disponible.isChecked()
        
        nuevo_producto = Producto(codigo, nombre, precio, cantidad, disponible)
        
        self.inventario.registrar_producto(nuevo_producto)
        
        
        self.mensaje.setIcon(QMessageBox.Information)
        self.mensaje.setText('El producto se ha creado de manera satisfatoria')
        self.mensaje.exec_()
        
        self.ui.txt_codigo.setText('1')
        self.ui.txt_nombre.setText('')
        self.ui.txt_precio.setText('1')
        self.ui.spx_cantidad.setValue(1)
        self.ui.chk_disponible.setCheckState(False)
        
            
        
        
class ProductoVender(QWidget):
    def __init__(self, inventario):
        super().__init__()
        
        
        self.inventario = inventario
        
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_ProductoVender()
        self.ui.setupUi(self)
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setWindowTitle('mensaje')
        self.mensaje.setIcon(QMessageBox.Warning)
        
        self.ui.txt_codigo.setValidator(QIntValidator(1, 1000000, self))
        self.ui.spx_cantidad.setMinimum(1)
        
        self.ui.btn_vender.clicked.connect(self.vender)
        
        
        
    def vender(self):
        
        cantidad = self.ui.spx_cantidad.value()
        
        try:
            codigo = int(self.ui.txt_codigo.text())
        except:
            self.mensaje.setText('El campo codigo es obligatorio.')
            self.mensaje.exec_()
            return
        
        producto = self.inventario.buscar_producto(codigo)
        
        if producto is None:
            self.mensaje.setText('No existe un producto con el codigo suministrado')
            self.mensaje.exec_()
            return
        
        if producto.disponible is True:
        
            if cantidad <= producto.cantidad:
                confirmacion = QMessageBox()
                texto = '¿Quiere vender el producto **{}** de codigo **{}**?'.format(producto.nombre, codigo)
                texto = markdown.markdown(texto)
                confirmacion.setText(texto)
                confirmacion.setIcon(QMessageBox.Question)
                confirmacion.setWindowTitle('confirmación')
                confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                boton_yes = confirmacion.button(QMessageBox.Yes)
                
                confirmacion.exec_()
                
                if confirmacion.clickedButton() == boton_yes:
                    venta = Venta(codigo, cantidad, producto.precio * cantidad)
                    self.inventario.realizar_venta(venta)
                    producto.cantidad -= cantidad
                    
                    self.mensaje.setText(markdown.markdown(f'Se ha vendido el producto **{producto.nombre}** \n\n'
                                                           f'Total de la venta (sin iva): **{venta.total_sin_iva}**'
                                                           f'\n\nUnidades restantes: **{producto.cantidad}**'))
                    
                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.exec_()
                else:
                    self.mensaje.setText('No se ha vendido el producto {}'.format(producto.nombre))
                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.exec_()
                    
            else:
                self.mensaje.setText(markdown.markdown(f'No hay suficientes cantidades del producto {producto.nombre}\nquedan {producto.cantidad} unidades'))
                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.exec_()
                return
                
        
        else:
            self.mensaje.setText(markdown.markdown(f'el producto **{producto.nombre}** no está diponible para la venta'))
            self.mensaje.setIcon(QMessageBox.Information)
            self.mensaje.exec_()
            return
        
        
class ProductoBuscar(QWidget):
    def __init__(self, inventario):
        super().__init__()
        
        self.inventario = inventario
        self.inicializarGui()
            
            
    def inicializarGui(self):
        self.ui = Ui_ProductoBuscar()
        self.ui.setupUi(self)
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setWindowTitle('mensaje')
        
        self.ui.txt_codigo.setValidator(QIntValidator(1, 1000000, self))
        self.ui.chk_disponible.setCheckable(False)
        self.ui.btn_buscar.clicked.connect(self.buscar)
        
    def buscar(self):
        codigo = self.ui.txt_codigo.text()
        
        if len(codigo):
            codigo = int(codigo)
            producto = self.inventario.buscar_producto(codigo)
            
            if producto is None:
                self.mensaje.setText(f'El producto con codigo {codigo} no existe')
                self.mensaje.exec_()
                
            else:
                nombre = str(producto.nombre)
                precio = str(producto.precio)
                cantidad = str(producto.cantidad)
                disponible = producto.disponible
                
                self.ui.txt_nombre.setText(nombre)
                self.ui.txt_precio.setText(precio)
                self.ui.txt_cantidad.setText(cantidad)
                self.ui.chk_disponible.setCheckState(disponible)
        else:
            self.mensaje.setText('El campo codigo es obligatorio')
            self.mensaje.exec_()
            
        
class ProductoCambiarDisponibilidad(QWidget):
    def __init__(self, inventario):
        super().__init__()
        
        self.inventario = inventario
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_ProductoCambiarDisponibilidad()
        self.ui.setupUi(self)
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setWindowTitle('mensaje')
        
        self.ui.chk_disponibilidad.setDisabled(True)
        self.ui.txt_codigo.setValidator(QIntValidator(1, 1000000, self))
        self.ui.btn_buscar.clicked.connect(self.buscar)
        
    def buscar(self):
        codigo = int(self.ui.txt_codigo.text())
        
        self.producto = self.inventario.buscar_producto(codigo)
        
        if self.producto is None:
            self.mensaje.setText('No se encontró ningún producto con el codigo dado')
            self.mensaje.exec_()
            return
        else:
            self.ui.chk_disponibilidad.setDisabled(False)
            self.ui.chk_disponibilidad.stateChanged.connect(self.cambiar_disponibilidad)
    
    def cambiar_disponibilidad(self):
        disponible = self.ui.chk_disponibilidad.isChecked()
        
        self.producto.disponible = disponible
        
class ProductoAgregarUnidades(QWidget):
    def __init__(self, inventario):
        super().__init__()
        
        self.inventario = inventario
        
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_ProductoAgregarUnidades()
        self.ui.setupUi(self)
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setWindowTitle('mensaje')
        
        self.ui.txt_codigo.setValidator(QIntValidator(1,1000000, self))
        self.ui.btn_agregar_unidades.clicked.connect(self.agregar_unidades)
        
    def agregar_unidades(self):
        codigo = self.ui.txt_codigo.text()
        
        if len(codigo):
            cantidad = self.ui.spb_unidades.value()
            codigo = int(codigo)
            
            producto = self.inventario.buscar_producto(codigo)
            
            if producto is not None:
                confirmacion = QMessageBox()
                texto = markdown.markdown(f'¿Quiere agregar **{cantidad}** unidades al producto **{producto.nombre}**?')
                confirmacion.setText(texto)
                confirmacion.setIcon(QMessageBox.Question)
                confirmacion.setWindowTitle('Agregar')
                confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                boton_yes = confirmacion.button(QMessageBox.Yes)
                
                confirmacion.exec_()
                
                if confirmacion.clickedButton() == boton_yes:
                    producto.cantidad += cantidad
                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText(markdown.markdown(f'Se agregaron **{cantidad}** unidades al producto **{producto.nombre}**\n\n'
                                                           f'el producto ahora tiene **{producto.cantidad}** unidades'))
                    self.mensaje.exec_()
                    
            else:
                self.mensaje.setText(markdown.markdown(f'El producto de codigo **{codigo}** no existe'))
                self.mensaje.exec_()
        else:
            self.mensaje.setText('El campo codigo es obligatorio')
            self.mensaje.exec_()
            
        
        
        
class ReporteProductosMasVendidos(QWidget):
    def __init__(self, inventario):
        super().__init__()
        
        self.inventario = inventario
        
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_Reporte_top5()
        self.ui.setupUi(self)
        self.setWindowTitle('Reporte - Top 5 productos más vendidos')
        
        productos_mas_vendidos = self.inventario.top_5_mas_vendidos()
        
        for p in productos_mas_vendidos:
            venta = self.inventario.buscar_producto(p[0])
            id = p[0] #id
            nombre = venta.nombre
            cantidad = p[1] #cantidad
            total = int(p[1]) * float(venta.precio) #total
            venta_2 = self.inventario.datos_venta_gui(p[0])
            fecha = venta_2.fecha
            
            numeroFila = self.ui.tbl_top_5.rowCount()
            self.ui.tbl_top_5.insertRow(numeroFila)
            
            self.ui.tbl_top_5.setItem(numeroFila, 0, QTableWidgetItem(str(id)))
            self.ui.tbl_top_5.setItem(numeroFila, 1, QTableWidgetItem(str(nombre)))
            self.ui.tbl_top_5.setItem(numeroFila, 2, QTableWidgetItem(str(fecha)))
            self.ui.tbl_top_5.setItem(numeroFila, 3, QTableWidgetItem(str(cantidad)))
            self.ui.tbl_top_5.setItem(numeroFila, 4, QTableWidgetItem(str(total)))
class ReporteProductosMenosVendidos(QWidget):
    def __init__(self, inventario):
        super().__init__()
        
        self.inventario = inventario
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_Reporte_top5()
        self.ui.setupUi(self)
        
        self.setWindowTitle('Reporte - Top 5 productos más vendidos')
        
        productos_mas_vendidos = self.inventario.top_5_menos_vendidos()
        
        for p in productos_mas_vendidos:
            venta = self.inventario.buscar_producto(p[0])
            id = p[0] #id
            nombre = venta.nombre
            cantidad = p[1] #cantidad
            total = int(p[1]) * float(venta.precio) #total
            venta_2 = self.inventario.datos_venta_gui(p[0])
            fecha = venta_2.fecha
            
            numeroFila = self.ui.tbl_top_5.rowCount()
            self.ui.tbl_top_5.insertRow(numeroFila)
            
            self.ui.tbl_top_5.setItem(numeroFila, 0, QTableWidgetItem(str(id)))
            self.ui.tbl_top_5.setItem(numeroFila, 1, QTableWidgetItem(str(nombre)))
            self.ui.tbl_top_5.setItem(numeroFila, 2, QTableWidgetItem(str(fecha)))
            self.ui.tbl_top_5.setItem(numeroFila, 3, QTableWidgetItem(str(cantidad)))
            self.ui.tbl_top_5.setItem(numeroFila, 4, QTableWidgetItem(str(total)))
class ReporteRangoFecha(QWidget):
    def __init__(self, inventario):
        super().__init__()
        
        self.inventario = inventario
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_ReporteVentasRangoFecha()
        self.ui.setupUi(self)
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setWindowTitle('mensaje')
        self.mensaje.setIcon(QMessageBox.Warning)
        
        self.ui.btn_buscar.clicked.connect(self.buscar_ventas_rango_fecha)
        self.ui.dat_fecha_final.setMaximumDateTime(QDateTime.currentDateTime())
        self.ui.dat_fecha_inicio.setMaximumDateTime(QDateTime.currentDateTime())
        
    def buscar_ventas_rango_fecha(self):
        fecha_inicio = self.ui.dat_fecha_inicio.date()
        fecha_final = self.ui.dat_fecha_final.date()
        
        if fecha_inicio > fecha_final:
            self.mensaje.setText('la fecha inicio no  puede ser mayor que la fecha final')
            self.mensaje.exec_()
            return
        
        fecha_inicio = fecha_inicio.toString('yyyy-MM-dd')
        fecha_final = fecha_final.toString('yyyy-MM-dd')
        
        fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_final = datetime.datetime.strptime(fecha_final, '%Y-%m-%d')
        
        ventas_rango = self.inventario.ventas_rango_fecha(fecha_inicio, fecha_final)
        
        self.ui.tbl_ventas.setRowCount(0)
        for v in ventas_rango:
            codigo = str(v.codigo_producto)
            fecha = str(v.fecha)
            cantidad = str(v.cantidad)
            total = str(v.total_sin_iva)
            
            numeroFila = self.ui.tbl_ventas.rowCount()
            self.ui.tbl_ventas.insertRow(numeroFila)
            
            self.ui.tbl_ventas.setItem(numeroFila, 0, QTableWidgetItem(codigo))
            self.ui.tbl_ventas.setItem(numeroFila, 1, QTableWidgetItem(fecha))
            self.ui.tbl_ventas.setItem(numeroFila, 2, QTableWidgetItem(cantidad))
            self.ui.tbl_ventas.setItem(numeroFila, 3, QTableWidgetItem(total))
        
        
class ReporteListadoProductos(QWidget):
    def __init__(self, inventario):
        super().__init__()
        
        self.inventario = inventario 
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_Reporte_listado_productos()
        self.ui.setupUi(self)
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setWindowTitle('mensaje')
        self.mensaje.setIcon(QMessageBox.Information)
        
        self.ui.txt_buscar_id.setValidator(QIntValidator(1, 1000000, self))
        
        self.ui.btn_buscar.clicked.connect(self.buscar_id)
        
        self.datos_listado()
        
    def datos_listado(self):
        self.ui.tbl_listado.setRowCount(0)
            
        for p in self.inventario.productos:
            codigo = p.codigo
            nombre = p.nombre
            cantidad = p.cantidad
            valor = p.precio
            if p.disponible is True:
                disponible = 'Si'
            else:
                disponible = 'No'
            
            numeroFila = self.ui.tbl_listado.rowCount()
            self.ui.tbl_listado.insertRow(numeroFila)
            
            self.ui.tbl_listado.setItem(numeroFila, 0, QTableWidgetItem(str(codigo)))
            self.ui.tbl_listado.setItem(numeroFila, 1, QTableWidgetItem(str(nombre)))
            self.ui.tbl_listado.setItem(numeroFila, 2, QTableWidgetItem(str(cantidad)))
            self.ui.tbl_listado.setItem(numeroFila, 3, QTableWidgetItem(str(valor)))
            self.ui.tbl_listado.setItem(numeroFila, 4, QTableWidgetItem(str(disponible)))
            
    def buscar_id(self):
        codigo = self.ui.txt_buscar_id.text()
        
        if len(codigo):
            codigo = int(codigo)
            
            producto = self.inventario.buscar_producto(codigo)
            
            
            if producto is not None:
                codigo = producto.codigo
                nombre = producto.nombre
                cantidad = producto.cantidad
                valor = producto.precio
                if producto.disponible is True:
                    disponible = 'Si'
                else:
                    disponible = 'No'
                    
                self.ui.tbl_listado.setRowCount(0)
                
                self.ui.tbl_listado.insertRow(0)
                
                    
                self.ui.tbl_listado.setItem(0, 0, QTableWidgetItem(str(codigo)))
                self.ui.tbl_listado.setItem(0, 1, QTableWidgetItem(str(nombre)))
                self.ui.tbl_listado.setItem(0, 2, QTableWidgetItem(str(cantidad)))
                self.ui.tbl_listado.setItem(0, 3, QTableWidgetItem(str(valor)))
                self.ui.tbl_listado.setItem(0, 4, QTableWidgetItem(str(disponible)))
                
            else:
                self.mensaje.setText('No existe un producto con el codigo suministrado')
                self.mensaje.exec_()
                self.datos_listado()
                
        else:
            self.datos_listado()
            
def main():
    app = QApplication(sys.argv)
    ventana = GestorInventarioAplicacion()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()