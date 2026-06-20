import mail_read
import wake_on_lan


#main
if __name__ == "__main__":

    #MAC a Encender
    mac_addrd = "BC:5F:F4:A4:65:5C"
    time_sleep = 4
    counter = 5

    #Leo los correos
    lista_correos = mail_read.leer_y_eliminar_correos(False)
    # print(lista_correos)

    # Si hay correos
    if lista_correos is not None:
    
        # Debe Encender PC?
        found_encender = mail_read.procesa_correos(lista_correos)

        # Si debo encender
        if found_encender is not None:
            wake_on_lan.send_wake_on_lan_times(mac_addrd,counter,time_sleep)

            #Envio respuesta
            mail_read.respuesta_correo(found_encender)
           
        #Elimino correos
        lista_correos = mail_read.leer_y_eliminar_correos(True)    