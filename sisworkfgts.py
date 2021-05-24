#coding= latin-1 
import csv
import string
import mysql.connector as msql
from mysql.connector import Error
from math import*
from string import* 
from datetime import datetime

#Conecatar com o banco BD_ACAOFGTS
try:
    conn = msql.connect(host='localhost', user='chico',password='chic@oSQL2020', database ='bd_acaofgts',
                              auth_plugin='mysql_native_password',charset='utf8')
    cursor = conn.cursor()
    if conn.is_connected():        
        print("database is created")
except Error as e:
    print("Error while connecting to MySQL", e)

# Abre arquivo csc com os dados do trabalharo para atualização
#file = "C:\\Users\\fasso\OneDrive\\Documents\\temp\\FGTS Francisco\\indicesinpc.csv"
file = "C:\\Users\\chico\OneDrive\\Documents\\temp\\FGTS Francisco\\indicesinpc.csv"
openFile = open(file,'r')
lin=0


#il_ intem da lista = Index Lista(il_)
il_trabalhador=[]
il_CPFtrabalhador=[]
il_emailtrabalhador=[]
il_senhatrabalhador=[]
il_datacadastro=[]
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
    print ('   6 - Buscar CSV e atualizar dados(Gravar atualização)') 
    print ('   7 - listar vinculo Trabalhador X Empresa X conta') 
    print ('   8 - Data Sys') 
    print ('   15 - Sair') 
    opt = input('Digite a opçao desejada: ') 
    return opt 
  
def adicionar_trabalhador ():
    trabalhador = str(input("Nome:"))
    il_trabalhador=trabalhador.upper()
    if il_trabalhador in list_trabalhador:
        print('trabalhador já Cadastrado !')
    else:
        CPFtrabalhador = str(input("CPF:"))
        carttrabalho = str(input("Num. Carteira Trabalho:"))
        pisPASEP = str(input("Pis/PASEP:"))
        il_CPFtrabalhador=CPFtrabalhador
        emailtrabalhador = str(input("E-mail:"))
        il_emailtrabalhador=emailtrabalhador
        senhatrabalhador = str(input("Senha:")) 
        il_senhatrabalhador = senhatrabalhador
        il_datacadastro = ver_date()
        list_trabalhador.append(il_trabalhador)
        list_trabalhador.append(il_CPFtrabalhador)
        list_trabalhador.append(il_emailtrabalhador)
        list_trabalhador.append(il_senhatrabalhador)
        list_trabalhador.append(il_datacadastro)
        strSql='insert pessoas (Nome,cpf,CarteiraTrabalho,PISPASEP,email,senha,DataCadastro) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        #print(strSql)
        listar_trabalhador (1)
        cursor.execute(strSql,(il_trabalhador,il_CPFtrabalhador,carttrabalho,pisPASEP,il_emailtrabalhador,il_senhatrabalhador,il_datacadastro))
        conn.commit()
        print('Trabalhador ',il_trabalhador, ' cadastrado!') 
    pass 

def adicionar_Empresa():
    empresa = str(input("Nome:"))
    il_empresa=empresa.upper()
    if il_empresa in list_empresa:
        print('Empresa já Cadastrado !')
    else:
        CodigoEmpresa = str(input("Codigo:"))
        cnpjEmresa= str(input("CNPJ:"))
        inscricao = str(input('Inscricao FGTS:'))
        strSql='insert Empresas (Empresa,CodigoEmpresa,cnpj,inscricao) values (%s,%s,%s,%s)'
        cursor.execute(strSql,(empresa,CodigoEmpresa,cnpjEmresa,inscricao))
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

    cnpj=str(input("Digite o Cnpj da Empresa:"))
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
    
    contaFGTS = input("Numero Conta FGTS:")
    dataOpcao = input("Data Opção:")
    categoria = input("Categoria FGTS:")
    tipoConta = input("Tipo Conta:")
    strSql='insert trabalhadordadosfgts (NumeroContaFGTS,DataOpcao,Categoria,TipoConta,Empresas_Id,Pessoas_ID) values (%s,%s,%s,%s,%s,%s)'
    cursor.execute(strSql,(contaFGTS,dataOpcao,categoria,tipoConta,id_Empresa,id_trabalhador))
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
        strSql= 'Select Id,Empresa,CodigoEmpresa,CNPJ,inscricao from Empresas'
    else:
        
        strSql= 'Select Id,Empresa,CodigoEmpresa,CNPJ,inscricao from Empresas where cnpj = %s'
    
    cursor.execute(strSql,_par)

    linhas = cursor.fetchall()
    print("Número total de registros retornados: ", cursor.rowcount)

    print("\nMostrando os autores cadastrados")
    for linha in linhas:
        print('----------------------------------------------------------------------------------------',"\n")
        print("Id:", linha[0])        
        print("CNPJ:", linha[3])
        print("Nome:", linha[1])
        print("Código Empresa:", linha[2])
        print("Inscricao:", linha[4])
        print('----------------------------------------------------------------------------------------',"\n")
    pass

def listar_Vinculo_Trabalhador_FGTS():
    NumeroContaFGTS=str(input("Digite o numero da conta do FGTS do trabalhador:"))
    strSql= "SELECT T3.ID,T3.NumeroContaFGTS,T1.ID,T1.CPF,T1.Nome,T2.ID,T2.CNPJ,T2.Empresa \
            from (trabalhadordadosfgts as T3 inner join pessoas as T1 on T3.Pessoas_ID=T1.ID) inner join Empresas T2 on T3.empresas_Id = T2.ID \
            where NumeroContaFGTS ='%s'" % NumeroContaFGTS
    cursor.execute(strSql)
    linhas = cursor.fetchall()
    if cursor.rowcount>0:
        for linha in linhas:
            id_trabalhador = linha[2]
            id_Empresa = linha[5]
            id_trabalhadorfgts = linha[0]
            print('\n******************************---------------------------------**********************************')
            print(id_trabalhadorfgts, 'indice da tabela vinculo trabalhador')
            print(id_trabalhador)
            print(linha[4])
            print(linha[7],"\n")
    else:
        print('Trabalhador não cadastrado') 
    #file = "C:\\Users\\chico\OneDrive\\Documents\\temp\\FGTS Francisco\\creditojan.csv"
    #file = "C:\\Users\\fasso\OneDrive\\Documents\\temp\\FGTS Francisco\\creditojan.csv"
    #file = "C:\\Users\\chico\OneDrive\\Documents\\temp\\FGTS erick\\creditojan.csv"
    #file = "C:\\Users\\chico\OneDrive\\Documents\\temp\\FGTS marcelo\\creditojan 4674.csv"
    #file = "C:\\Users\\chico\OneDrive\\Documents\\temp\\FGTS marcelo\\creditojan 7529.csv"
    file = "C:\\Users\\chico\OneDrive\\Documents\\temp\\FGTS marcelo\\creditojan 30423.csv"
    openFile = open(file,'r')
    lin=0
    totalCorrigido=0
    valorCreditado=0
    with openFile as arq:
        linhas = csv.DictReader(arq,delimiter = ';',fieldnames=['Data','Lancamentos','Valor','Total'])
        linhas.__next__()
        for linha in linhas: 
            lin+=1
            vetDate=linha['Data'].strip().split("/")
            mes=int(vetDate[1].strip())
            ano=int(vetDate[2].strip())
            valorCreditado = float(linha['Valor'].replace(',', '.').strip()) 
            if ano>=1999:
                print(id_trabalhadorfgts, 'indice da tabela vinculo trabalhador')
                print(vetDate)
                print(mes)
                print(ano)
                print(valorCreditado)
                strSql="SELECT Id,Mes,Ano,IndiceJAM3,indiceINPC,Juros3,NovoIndice FROM indiceinpc where mes= %s and ano = %s"
                cursor.execute(strSql,(mes,ano))
                result = cursor.fetchall()
                for i in result:
                    Id_indiceINPC = i[0]
                    totalCorrigido = totalCorrigido                        
                    print(Id_indiceINPC)
                    print(i[1])
                    print(i[2])
                    #indiceJAM3 = "%.2f" % i[3]
                    indiceJAM3 = i[3]
                    print(indiceJAM3)
                    print(i[4])
                    print(i[5])
                    novoIndice = i[6]
                    print(novoIndice)  
                    #creditoJan = decimal(2.10) creditoJan              
                    #----------------------------------------------------------------------------------------------------------------------
                    creditoJan = valorCreditado/indiceJAM3 
                    #
                    print('Credito do mes FGTDS ',  creditoJan )
                    newCredito = creditoJan * novoIndice
                    #newCredito = "%.2f" %newCredito
                    print('Novo Valor do Credito do mes FGTDS ',  newCredito )
                    diferencaCredito = newCredito - valorCreditado 
                    #diferencaCredito = "%.2f" %diferencaCredito  
                    print('Novo Valor da diferenca Credito do mes FGTDS ',  diferencaCredito )
                    novaCorrecao = totalCorrigido * novoIndice
                    #novaCorrecao = "%.2f" %novaCorrecao
                    print('Correção INPC + 3 % aa', novaCorrecao)
                    totalCorrigido = totalCorrigido + diferencaCredito + novaCorrecao
                    ValortotalCorrigido = "%.2f" %totalCorrigido
                    print('Valor Corrigido',totalCorrigido)
                    strSql='INSERT INTO fgtsatualizarpessoa (Mes,Ano,ValorJAM,ValorCreditado,NovoCredito,DiferencaCredito,Correcao,TotalCorrigido,indiceinpc_Id, \
                            trabalhadordadosfgts_ID,trabalhadordadosfgts_Pessoas_ID,trabalhadordadosfgts_empresas_Id) \
                            VALUES( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    
                    print(id_trabalhadorfgts, 'indice da tabela vinculo trabalhador II')
                    cursor.execute(strSql,(mes,ano,indiceJAM3,"%.2f" %valorCreditado,newCredito,"%.2f" %diferencaCredito,"%.2f" %novaCorrecao,ValortotalCorrigido,Id_indiceINPC,id_trabalhadorfgts,id_trabalhador,id_Empresa))
                    conn.commit()
                    print('\n******************************---------------------------------**********************************')


    print(lin)
    conn.close()
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
    return strdata
    print(today)
    print('n/')
    print ('STR_TO_DATE("',strdata,'","%d/%m/%Y")')
print('inicio do sistema') 

print('/n')

le_trabalhador() 
opcao = menu() 
while opcao != '15': 
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
    elif opcao == '6':
        listar_Vinculo_Trabalhador_FGTS()
    elif opcao == '8':
        datasis = ver_date()
        print(datasis)

    opcao = menu() 


