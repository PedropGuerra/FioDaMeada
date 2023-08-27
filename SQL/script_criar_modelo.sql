USE sql10642707; /*Ambiente de Produção: Mudar para "Fio da Meada"*/

create table SendPulse_Flows (
    ID_Flow_DB int auto_increment NOT NULL,
    ID_Flow_API varchar(2048),
    Nome_Flow varchar(100),
    Data_Registro date,
    PRIMARY KEY (ID_Flow_DB)
);

create table Metodo_Raspagem_Noticias (
    ID_Metodo_Coleta int auto_increment NOT NULL,
    Nome_Metodo_Coleta char(10),
    PRIMARY KEY (ID_Metodo_Coleta)
);

create table Preferencia_Usuarios (
    ID_Pref_Usuario int auto_increment NOT NULL,
    Nome_Preferencia char(15),
    PRIMARY KEY(ID_Pref_Usuario)
);

create table Parceiros (
    ID_Parceiro int auto_increment NOT NULL,
    Nome_Parceiro varchar(20) NOT NULL,
    Data_Registro_DB date, 
    Link_Parceiro varchar(2048) NOT NULL,
    Nome_Responsavel char(24),
    Contato_Responsavel varchar(13),
    Licenca_Distrib varchar(15),
    ID_Metodo_Coleta tinyint(1) NOT NULL, /*1: Raspagem, 2:Feed RSS, 3:Manual*/
    Tags_HTML_Raspagem varchar(2048) NOT NULL, /*Headline:tag,Texto_Principal:tag...*/
    Ult_Raspagem date,
    Status boolean,
    FOREIGN KEY (ID_Metodo_Coleta) REFERENCES Metodo_Raspagem_Noticias(ID_Metodo_Coleta),
    PRIMARY KEY (ID_Parceiro)
);

create table Noticias (
    ID_Noticia int auto_increment NOT NULL,
    ID_Parceiro int NOT NULL,
    Link_Publicacao varchar(2048) NOT NULL,
    Data_Publicacao date(0) NOT NULL,
    Headline_Publicacao text NOT NULL,
    Resumo_Publicacao text NOT NULL, /*https://www.turbinetext.com/pt/resumo*/
    Tema_Publicacao char(24) NOT NULL,
    ID_Pref_Usuario int NOT NULL,
    Data_Publicacao_Parceiro date NOT NULL, /*Data da publicação da notícia no portal do parceiro*/
    Data_Registro_DB date, /*Data de registro no Banco de Dados*/
    FOREIGN KEY (ID_Parceiro) REFERENCES Parceiros(ID_Parceiro),
    FOREIGN KEY (ID_Pref_Usuario) REFERENCES Preferencia_Usuarios(ID_Pref_Usuario),
    PRIMARY KEY(ID_Noticia)
);


create table Envios (
    ID_Transacao_Envio int auto_increment NOT NULL,
    ID_Envio int NOT NULL,
    ID_Pref_Usuario int NOT NULL,
    ID_Noticia int NOT NULL,
    ID_Flow_DB int NOT NULL,
    Data_Envio datetime NOT NULL,
    FOREIGN KEY (ID_Noticia) REFERENCES Noticias(ID_Noticia),
    FOREIGN KEY (ID_Pref_Usuario) REFERENCES Preferencia_Usuarios(ID_Pref_Usuario),
    FOREIGN KEY (ID_Flow_DB) REFERENCES SendPulse_Flows(ID_Flow_DB),
    PRIMARY KEY (ID_Transacao_Envio)
);

create table Usuarios (
    ID_Usuario int auto_increment NOT NULL,
    Primeiro_Nome char(12),
    Ult_Nome char(12),
    Data_Registro date,
    DDD char(3),
    Telefone_Celular varchar(12),
    Tipo_WhatsApp boolean, /*Business ou Pessoal*/
    Data_Ult_Interacao datetime,
    Status char(1), /*Ativo/Inativo/Unsubscribed/BlockedByUser*/
    Data_Nasc date, /*Formato DD/MM/AAAA*/
    Pref_Usuario1 int NOT NULL,
    Pref_Usuario2 int NOT NULL,
    Pref_Usuario3 int NOT NULL,
    FOREIGN KEY (Pref_Usuario1) REFERENCES Preferencia_Usuarios(ID_Pref_Usuario),
    FOREIGN KEY (Pref_Usuario2) REFERENCES Preferencia_Usuarios(ID_Pref_Usuario),
    FOREIGN KEY (Pref_Usuario3) REFERENCES Preferencia_Usuarios(ID_Pref_Usuario),
    PRIMARY KEY (ID_Usuario)
);