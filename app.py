from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
import mysql.connector
import matplotlib.pyplot as plt 
import openpyxl


	



db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port=3306,
    database="bot_telegram",
)
#app = Flask(__name__)
#mysql = MySQL(app)




def grafico(update,context):
	x = [15, 25, 25, 30, 5]
	labels = ['Very Likely', 'Likely', 'Unsure', 'Unlikely', 'Very Unlikely']
	colors = ['tab:blue', 'tab:cyan', 'tab:gray', 'tab:orange', 'tab:red']

	fig, ax = plt.subplots()
	ax.pie(x, labels = labels, colors = colors)
	ax.set_title('Survery responses')

	context.bot.send_message(update.message.chat_id,plt.show())




#update.message.text() resive el texto
def help(update, context):
	''' comandos '''
	
	context.bot.send_message(update.message.chat_id,"Bienvenido \n  estos son nuestros comandos \n /mostrar_ingresos : este comando te permitira saber todos los ingresos que has tenido el mes actual \n /ingresar_monto : con este podras realizar el guardado de tu monto para llevarlo en el registro,recuerda ingresar el monto junto a la descripcion y al comando poner  fecha a tu monto ingresado  formato 2022-05-25 ejemplo(5000 venta_arroz 2022-05-25 )\n /sumar_gastos con este comando conoceras todo lo que has gastado")
def suma(update,context):
    	
    #context.bot.send_message(update.message.chat_id,"Hola, por favor escribenos en numeros sin espacios ni comas el monto que deseas ingresar")

	

	cursor = db.cursor()
	cursor.execute("SELECT SUM(monto_a_ingresar)AS suma FROM ingresos ")
	suma=cursor.fetchone()
	db.commit()

	#update.message.reply_text("por favor utilice dos numeros",suma[0])
	context.bot.send_message(update.message.chat_id,"La sumatoria de tus ingresos es: "+str(suma[0]))

def ingresar_monto(update,context):
    	
    #context.bot.send_message(update.message.chat_id,"Hola, por favor escribenos en numeros sin espacios ni comas el monto que deseas ingresar")

	numero1 = int(context.args[0])
	fecha = context.args[1]
	descripcion=context.args[2]

	cursor = db.cursor()
	cursor.execute("INSERT INTO ingresos (monto_a_ingresar,fecha,descripcion)VALUES (%s,%s,%s)", (numero1,descripcion,fecha))
	db.commit()

def ingresos_mes(update, context):
	cursor=db.cursor()
	cursor.execute("SELECT monto_a_ingresar,descripcion,fecha FROM ingresos")

	mes=cursor.fetchall()
	texto=""
	for database in mes:
		texto = texto + '\n'+database[0]+" "+database[1]+" "+str(database[2])
		print(database)
	context.bot.send_message(update.message.chat_id,"Hola, acontinuacion te mostraremos los ingresos de este mes  "+texto)
	
    	
def start(update, context):
	''' START '''
	# Enviar un mensaje a un ID determinado.
	context.bot.send_message(update.message.chat_id, "Hola, bienvenido a tu bot de confianza, llevare un registro de tus ingresos y gastos para que puedas organizarte mejor, escribe /help para saber como funciono")

def gasto(update,context):
	numero1 = int(context.args[0])
	fecha = context.args[1]
	descripcion=context.args[2]

	cursor = db.cursor()
	cursor.execute("INSERT INTO gastos (ingreso_gasto,fecha,descripcion)VALUES (%s,%s,%s)", (numero1,descripcion,fecha))
	db.commit()

def mostrar_gastos(update,context):
	cursor=db.cursor()
	cursor.execute("SELECT ingreso_gasto,descripcion,fecha FROM gastos")

	mes=cursor.fetchall()
	texto=""
	for database in mes:
		texto = texto + '\n'+database[0]+" "+database[1]+" "+str(database[2])
		print(database)
	context.bot.send_message(update.message.chat_id,"Hola, acontinuacion te mostraremos los ingresos de este mes  "+texto)



def suma_gasto(update,context ):
	cursor = db.cursor()
	cursor.execute("SELECT SUM(ingreso_gasto)AS GASTOS FROM gastos ")
	suma=cursor.fetchone()
	db.commit()
	#if suma[0]>2000:
	#	context.bot.send_message(update.message.chat_id,"Wao, has gastado demasiado, empieza a ahorrar un poco")
	#update.message.reply_text("por favor utilice dos numeros",suma[0])
	context.bot.send_message(update.message.chat_id,"La sumatoria de tus Gastos es: "+str(suma[0]))




def main():
	TOKEN="5368500412:AAFZSD-TXNe_MWOaLQbcFc6AzpqCDYxTIYQ"
	updater=Updater(TOKEN, use_context=True)
	dp=updater.dispatcher

	# Eventos que activarán nuestro bot.
	dp.add_handler(CommandHandler('start',	start))
	dp.add_handler(CommandHandler('help',	help))
	dp.add_handler(CommandHandler('mostrar_gastos',	mostrar_gastos))
	dp.add_handler(CommandHandler('mostrar_ingresos',	ingresos_mes))
	dp.add_handler(CommandHandler('ingresar_monto',	ingresar_monto))
	dp.add_handler(CommandHandler('ingresar_gasto',	gasto))
	dp.add_handler(CommandHandler('suma_ingreso',	suma))
	dp.add_handler(CommandHandler('sumar_gastos',	suma_gasto))
	dp.add_handler(CommandHandler('grafico',	grafico))

	# Comienza el bot
	#dp.add_handler(MessageHandler(Filters.text, ))
	updater.start_polling()
	# Lo deja a la escucha. Evita que se detenga.
	updater.idle()

if __name__ == '__main__':
	main()


