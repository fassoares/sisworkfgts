#coding= latin-1 
import string
import mysql.connector as msql
from mysql.connector import Error
from math import*
from string import* 
from datetime import datetime

#Conecatar com o banco BD_ACAOFGTS
try:
    conn = msql.connect(host='localhost', user='chico',password='chic@oSQL2020', database ='bd_acaofgts',charset='utf8')
    cursor = conn.cursor()
    if conn.is_connected():        
        print("database is created")
except Error as e:
    print("Error while connecting to MySQL", e)

# Abre arquivo csc com os dados do trabalharo para atualização
file = "C:\\Users\\fasso\OneDrive\\Documents\\temp\\FGTS Francisco\\indicesinpc.csv"
openFile = open(file,'r')
lin=0


#il_ intem da lista = Index Lista(il_)
il_trabalhador=[]
il_CPFtrabalhador=[]
il_emailtrabalhador=[]
il_senhatrabalhador=[]
il_datacadastro=[]
#list_trabalhador=[il_trabalhador,il_CPFtrabalhador,il_emailtrabalhador,il_senhatrabalhador,il_datacadastro] 
list_trabalhador=[il_trabalhador,il_CPFtrabalhador,il_emailtrabalhador,il_senhatrabalhador] 
list_empresa=[]
empresa=''
trabalhador=''
id_trabalhador=0
id_Empresa=0
CPFtrabalhador=''
emailtrabalhador=''
senhatrabalhador=''
 
#A função que ira ser usada 
def menu (): 
    print ('Menu:') 
    print ('   1 - Cadastrar Trabalhador') 
    print ('   2 - Listar Trabalhador') 
    print ('   3 - cadastrar Empresa') 
    print ('   4 - listar Empresa') 
    print ('   5 - vincular trabalhador e sua conta a Empresa') 
    print ('   6 - listar vinculo Trabalhador X Empresa X conta') 
    print ('   7 - Buscar CSV e atualizar dados(Gravar atualização)') 
    print ('   9 - Sair') 
    opt = input('Digite a opçao desejada: ') 
    return opt 
  
def adicionar_trabalhador ():
    trabalhador = str(input("Nome:"))
    il_trabalhador=trabalhador.upper()
    if il_trabalhador in list_trabalhador:
        print('trabalhador já Cadastrado !')
    else:
        CPFtrabalhador = str(input("CPF:"))
        il_CPFtrabalhador=CPFtrabalhador
        emailtrabalhador = str(input("E-mail:"))
        il_emailtrabalhador=emailtrabalhador
        senhatrabalhador = str(input("Senha:")) 
        il_senhatrabalhador = senhatrabalhador
        il_datacadastro = datetime.now()
        list_trabalhador.append(il_trabalhador)
        list_trabalhador.append(il_CPFtrabalhador)
        list_trabalhador.append(il_emailtrabalhador)
        list_trabalhador.append(il_senhatrabalhador)
        list_trabalhador.append(il_datacadastro)
        strSql='insert pessoas (Nome,cpf,email,senha) VALUES (%s,%s,%s,%s)'
        print(strSql)
        listar_trabalhador ()
        cursor.execute(strSql,(il_trabalhador,il_CPFtrabalhador,il_emailtrabalhador,il_senhatrabalhador))
        conn.commit()
        print('Trabalhador ',il_trabalhador, ' cadastrado!') 
    pass 

def adicionar_Empresa():
    empresa = str(input("Nome:"))
    il_empresa=empresa.upper()
    if il_empresa in list_empresa:
        print('Empresa já Cadastrado !')
    else:
        empresaCodigo = str(input("Codigo:"))
        cnpjEmresa= str(input("CNPJ:"))
        strSql='insert Empresas (Empresa,Codigo,cnpj) values (%s,%s,%s)'
        cursor.execute(strSql,(empresa,empresaCodigo,cnpjEmresa))
        conn.commit()
        print('Trabalhador ',empresa, ' cadastrado!') 
    pass 

def remover_trabalhador (): 
    trabalhador=str(input("Digite o nome do trabalhador:"))
    trabalhador=trabalhador.upper()
    if trabalhador in list_trabalhador:
        list_trabalhador.remove(trabalhador) 
        print('trabalhador Removido')
    else:
        print('Esse trabalhador Não Está Cadastrado') 
    pass 
  
def adicionar_TrabalhadorEmpresa ():
    cpf=str(input("Digite o CPF do trabalhador:"))
    strSql= "SELECT ID,CPF,Nome,email,senha,DataCadastro FROM pessoas where CPF ='%s'" % cpf
    cursor.execute(strSql)
    linhas = cursor.fetchall()
    if cursor.rowcount>0:
        for linha in linhas:
            id_trabalhador = linha[0]
            print("\n",id_trabalhador)
            print(linha[1])
            print(linha[2],"\n")
    else:
        print('Trabalhador não cadastrado')

    cnpj=str(input("Digite o Cnpj do trabalhador:"))
    strSql= "SELECT ID,cnpj,Empresa FROM Empresas where CNPJ ='%s'" % cnpj
    cursor.execute(strSql)
    linhas = cursor.fetchall()
    if cursor.rowcount>0:
        for linha in linhas:
            id_Empresa = linha[0]
            print("\n",id_Empresa)
            print(linha[1])
            print(linha[2],"\n")
    else:
        print('Empresa não cadastrado')
    ContaFGTS = input("Numero Conta FGTS:")
    CarteiraTrabalho = input("Numero Conta Carteira Trabalho:")
    Inscricao = input("Numero Inscrição FGTS:")
    NumeroConta = input("Numero Conta FGTS:")
    DataOpcao = input("Data cadastro da conta FGTS:")
    Categoria = input("Categoria FGTS:")
    TipoConta = input("Tipo Conta FGTS:")
    strSql='insert trabalhadordadosfgts (ContaFGTS,CarteiraTrabalho,Inscricao,NumeroConta,DataOpcao,Categoria,TipoConta,Empresa_Id,Pessoas_ID) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(strSql,(ContaFGTS,CarteiraTrabalho,Inscricao,NumeroConta,DataOpcao,Categoria,TipoConta,id_Empresa,id_trabalhador))
    conn.commit()
    pass 

def listar_trabalhador (_par): 
    if (_par=='1'):
        strSql= 'SELECT ID,CPF,Nome,email,senha,DataCadastro FROM pessoas'
    else:        
        strSql= "SELECT ID,CPF,Nome,email,senha,DataCadastro FROM pessoas where CPF ='%s'" % _par
    cursor.execute(strSql)
    linhas = cursor.fetchall()
    print("Número total de registros retornados: ", cursor.rowcount)
    print("\nMostrando o(s) Trabalhador(es)")
    for linha in linhas:
        print('----------------------------------------------------------------------------------------',"\n")
        print("Id:", linha[0])        
        print("CPF:", linha[1])
        print("Nome:", linha[2])
        print("E-mail:", linha[3])
        print('----------------------------------------------------------------------------------------',"\n")
    
    pass 

def listar_Empresa(_par):
    
    if (int)(_par=='1'):
        strSql= 'Select id,Empresa,codigo,cnpj from Empresas'
    else:
        print(_par,'estou aqui!')
        strSql= 'Select Id, Empresa, Codigo, CNPJ from Empresas where cnpj = %s'
    
    cursor.execute(strSql,_par)

    linhas = cursor.fetchall()
    print("Número total de registros retornados: ", cursor.rowcount)

    print("\nMostrando os autores cadastrados")
    for linha in linhas:
        print('----------------------------------------------------------------------------------------',"\n")
        print("Id:", linha[0])        
        print("CNPJ:", linha[3])
        print("Nome:", linha[1])
        print("Código:", linha[2])
        print('----------------------------------------------------------------------------------------',"\n")
    pass

def verificar_situacao ():
    trabalhador = str(input("Digite o nome do trabalhador: "))
    pass 
  
def le_trabalhador(): 
    print(list_trabalhador) 
    pass 
def ver_date():
    today = datetime.now()
    strdata=today.strftime("%d/%m/%Y")
    strdata=strdata.strip()
    #strdata='STR_TO_DATE(',strdata,'"%d/%m/%Y")'
  
    print(today)
    print('n/')
    print ('STR_TO_DATE("',strdata,'","%d/%m/%Y")')
print('inicio do sistema') 

print('/n')

le_trabalhador() 
opcao = menu() 
while opcao != '9': 
    if opcao == '1': 
        adicionar_trabalhador()
    elif opcao == '2':  
        print (' Digite 1, lista todas as empresas') 
        print (' Digite o CPF busca a empresa')
        paramentro = input("dado da pesquisa:")
        listar_trabalhador(paramentro)
    elif opcao == '3':  
        adicionar_Empresa()
    elif opcao == '4':         
        print (' digite 1, lista todas as empresas') 
        print (' Digite o CNPJ busca a empresa')
        paramentro = input("dado da pesquisa:")  
        listar_Empresa(paramentro)
    elif opcao == '5':
        adicionar_TrabalhadorEmpresa()
    opcao = menu() 


