from .producto import Producto
from .venta import Venta
from collections import Counter

class Inventario():
    def __init__(self):
        self.productos = []
        self.ventas = []
        
    def registrar_producto(self, producto):
        """
        registra un nuevo producto en el inventario
        
        Paramenters:
        productos: lista de productos en el inventario
        producto: producto a agregar al inventario
        """
        self.productos.append(producto)
        
    def realizar_venta(self, venta):
        """
        crea una nueva venta
        
        Paramenters:
        ventas: lista de las ventas realizadas hasta el momento
        venta: venta recién realizada
        """
        self.ventas.append(venta)
        
    def buscar_producto(self, codigo):
        """
        Busca un producto a partir de su id.
        
        Parameters:
        productos: lista de productos en el inventario.
        codigo: id del producto a buscar.
        
        Returns:
        el producto encontrado, si no se encuentra se retorna None.
        """
        for p in self.productos:
            if p.codigo == codigo:
                return p
        return None

    def disponibilidad(self, producto):
        """
        cambia el estado de un producto
        
        Parameters:
        producto: producto por el que se cambiará su estado
        """
        producto.disponible =  not producto.disponible
        
    def ventas_rango_fecha(self, fecha_inicio, fecha_final):
        """
        obtiene las ventas que se han realizado en un rango de fecha
        
        Parameters:
        ventas: lista de ventas realizadas hasta el momento
        fecha_inicio: fecha de inicio del rango
        fecha_final: fecha final del rango
        
        Returns.
        lista de ventas realizadas en el rango especificado
        """
        ventas_rango = list()
        for v in self.ventas:
            if fecha_inicio <= v.fecha <= fecha_final:
                ventas_rango.append(v)
                
        return ventas_rango

    def top_5_mas_vendidos(self):
        """
        obtiene el top 5 de los productos más vendidos
        
        Parameters:
        ventas: lista de las ventas realizadas hasta el momento
        
        Returns:
        lista de tuplas (id, cantidad_total_venta) de los 5 productos más vendidos.
        """
        conteo_ventas = {}
        
        for v in self.ventas:
            if v.codigo_producto in conteo_ventas:
                conteo_ventas[v.codigo_producto] += v.cantidad
            else:
                conteo_ventas[v.codigo_producto] = v.cantidad
        conteo_ventas = {k: v for k, v in sorted(conteo_ventas.items(), key = lambda item: item[1], reverse = True)}
        
        contador = Counter(conteo_ventas)
        
        return contador.most_common(5) #[(1, 20), (10,15), (5, 10), (2,3),(8,2)]


    def top_5_menos_vendidos(self):
        """
        obtiene el top 5 de los productos menos vendidos
        
        Parameters:
        ventas: lista de las ventas realizadas hasta el momento
        
        Returns:
        lista de tuplas (id, cantidad_total_venta) de los 5 productos menos vendidos.
        """
        conteo_ventas = {}
        
        for v in self.ventas:
            if v.codigo_producto in conteo_ventas:
                conteo_ventas[v.codigo_producto] += v.cantidad
            else:
                conteo_ventas[v.codigo_producto] = v.cantidad
        conteo_ventas = {k: v for k, v in sorted(conteo_ventas.items(), key = lambda item: item[1])}
        
        contador = Counter(conteo_ventas)
        
        return contador.most_common()[:-6:-1]

    def mostrar_datos_producto(self, producto):
        """
        Muestra los datos particulares de un producto
        
        Parameters:
        Producto: Producto a consultar sus datos.
        """
        print('ID: %i' % producto.codigo)
        print('nombre: %s' % producto.nombre)
        print('Precio: %.2f' % producto.precio)
        print('Cantidad: %i' % producto.cantidad)
        print('¿Disponible?: %s' % ('Sí' if producto.disponible else 'No'))
        
        
    def mostrar_datos_venta(self, venta):
        """
        Muestra los datos particulares de una venta
        
        Parameters:
        venta: venta a consultar sus datos.
        """
        print('\nID Producto: %i' % venta.codigo_producto)
        print('fecha: %s' % venta.fecha)
        print('Cantidad: %i' % venta.cantidad)
        print('total sin IVA: $%.2f' % venta.total_sin_iva)
        print('total: $%.2f' % (venta.total_sin_iva * 1.19))
        print('\nDatos del producto:')
        self.mostrar_datos_producto(self.buscar_producto(venta.codigo_producto))
        
    def mostrar_datos_venta_producto(self, datos_venta):
        producto = self.buscar_producto(datos_venta[0])
        self.mostrar_datos_producto(producto)
        print('Cantidad vendida: %i' % datos_venta[1])
        
    def datos_venta_gui(self, codigo):
        for v in self.ventas:
            if v.codigo_producto == codigo:
                return v
        return None
    
            
        
