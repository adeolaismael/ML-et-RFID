/*
Script de déploiement pour PROJETContext-7c482fd8-c423-4f72-8cc1-131d23be3f1f

Ce code a été généré par un outil.
La modification de ce fichier peut provoquer un comportement incorrect et sera perdue si
le code est régénéré.
*/

GO
SET ANSI_NULLS, ANSI_PADDING, ANSI_WARNINGS, ARITHABORT, CONCAT_NULL_YIELDS_NULL, QUOTED_IDENTIFIER ON;

SET NUMERIC_ROUNDABORT OFF;


GO
:setvar DatabaseName "PROJETContext-7c482fd8-c423-4f72-8cc1-131d23be3f1f"
:setvar DefaultFilePrefix "PROJETContext-7c482fd8-c423-4f72-8cc1-131d23be3f1f"
:setvar DefaultDataPath "C:\Users\cafes\AppData\Local\Microsoft\Microsoft SQL Server Local DB\Instances\mssqllocaldb\"
:setvar DefaultLogPath "C:\Users\cafes\AppData\Local\Microsoft\Microsoft SQL Server Local DB\Instances\mssqllocaldb\"

GO
:on error exit
GO
/*
Détectez le mode SQLCMD et désactivez l'exécution du script si le mode SQLCMD n'est pas pris en charge.
Pour réactiver le script une fois le mode SQLCMD activé, exécutez ce qui suit :
SET NOEXEC OFF; 
*/
:setvar __IsSqlCmdEnabled "True"
GO
IF N'$(__IsSqlCmdEnabled)' NOT LIKE N'True'
    BEGIN
        PRINT N'Le mode SQLCMD doit être activé de manière à pouvoir exécuter ce script.';
        SET NOEXEC ON;
    END


GO
USE [$(DatabaseName)];


GO

IF (SELECT OBJECT_ID('tempdb..#tmpErrors')) IS NOT NULL DROP TABLE #tmpErrors
GO
CREATE TABLE #tmpErrors (Error int)
GO
SET XACT_ABORT ON
GO
SET TRANSACTION ISOLATION LEVEL READ COMMITTED
GO
BEGIN TRANSACTION
GO
PRINT N'Suppression de Clé étrangère [dbo].[FK_Histo_Hparam_Hyperparamètres_IdHParam]...';


GO
ALTER TABLE [dbo].[Histo_Hparam] DROP CONSTRAINT [FK_Histo_Hparam_Hyperparamètres_IdHParam];


GO
IF @@ERROR <> 0
   AND @@TRANCOUNT > 0
    BEGIN
        ROLLBACK;
    END

IF OBJECT_ID(N'tempdb..#tmpErrors') IS NULL
    CREATE TABLE [#tmpErrors] (
        Error INT
    );

IF @@TRANCOUNT = 0
    BEGIN
        INSERT  INTO #tmpErrors (Error)
        VALUES                 (1);
        BEGIN TRANSACTION;
    END


GO
PRINT N'Suppression de Clé étrangère [dbo].[FK_Histo_Hparam_Sauvegarde_IdSauvegarde]...';


GO
ALTER TABLE [dbo].[Histo_Hparam] DROP CONSTRAINT [FK_Histo_Hparam_Sauvegarde_IdSauvegarde];


GO
IF @@ERROR <> 0
   AND @@TRANCOUNT > 0
    BEGIN
        ROLLBACK;
    END

IF OBJECT_ID(N'tempdb..#tmpErrors') IS NULL
    CREATE TABLE [#tmpErrors] (
        Error INT
    );

IF @@TRANCOUNT = 0
    BEGIN
        INSERT  INTO #tmpErrors (Error)
        VALUES                 (1);
        BEGIN TRANSACTION;
    END


GO
PRINT N'Début de la régénération de la table [dbo].[Histo_Hparam]...';


GO
BEGIN TRANSACTION;

SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SET XACT_ABORT ON;

CREATE TABLE [dbo].[tmp_ms_xx_Histo_Hparam] (
    [IdHisto_HParam] INT           IDENTITY (1, 1) NOT NULL,
    [IdSauvegarde]   INT           NOT NULL,
    [IdHParam]       INT           NOT NULL,
    [SelectedValue]  VARCHAR (255) NOT NULL,
    CONSTRAINT [tmp_ms_xx_constraint_PK_Histo_Hparam1] PRIMARY KEY CLUSTERED ([IdHisto_HParam] ASC)
);

IF EXISTS (SELECT TOP 1 1 
           FROM   [dbo].[Histo_Hparam])
    BEGIN
        INSERT INTO [dbo].[tmp_ms_xx_Histo_Hparam] ([IdSauvegarde], [IdHParam], [SelectedValue])
        SELECT [IdSauvegarde],
               [IdHParam],
               [SelectedValue]
        FROM   [dbo].[Histo_Hparam];
    END

DROP TABLE [dbo].[Histo_Hparam];

EXECUTE sp_rename N'[dbo].[tmp_ms_xx_Histo_Hparam]', N'Histo_Hparam';

EXECUTE sp_rename N'[dbo].[tmp_ms_xx_constraint_PK_Histo_Hparam1]', N'PK_Histo_Hparam', N'OBJECT';

COMMIT TRANSACTION;

SET TRANSACTION ISOLATION LEVEL READ COMMITTED;


GO
IF @@ERROR <> 0
   AND @@TRANCOUNT > 0
    BEGIN
        ROLLBACK;
    END

IF OBJECT_ID(N'tempdb..#tmpErrors') IS NULL
    CREATE TABLE [#tmpErrors] (
        Error INT
    );

IF @@TRANCOUNT = 0
    BEGIN
        INSERT  INTO #tmpErrors (Error)
        VALUES                 (1);
        BEGIN TRANSACTION;
    END


GO
PRINT N'Création de Index [dbo].[Histo_Hparam].[IX_Histo_Hparam_IdHParam]...';


GO
CREATE NONCLUSTERED INDEX [IX_Histo_Hparam_IdHParam]
    ON [dbo].[Histo_Hparam]([IdHParam] ASC);


GO
IF @@ERROR <> 0
   AND @@TRANCOUNT > 0
    BEGIN
        ROLLBACK;
    END

IF OBJECT_ID(N'tempdb..#tmpErrors') IS NULL
    CREATE TABLE [#tmpErrors] (
        Error INT
    );

IF @@TRANCOUNT = 0
    BEGIN
        INSERT  INTO #tmpErrors (Error)
        VALUES                 (1);
        BEGIN TRANSACTION;
    END


GO
PRINT N'Création de Clé étrangère [dbo].[FK_Histo_Hparam_Hyperparamètres_IdHParam]...';


GO
ALTER TABLE [dbo].[Histo_Hparam] WITH NOCHECK
    ADD CONSTRAINT [FK_Histo_Hparam_Hyperparamètres_IdHParam] FOREIGN KEY ([IdHParam]) REFERENCES [dbo].[Hyperparamètres] ([IdHParam]);


GO
IF @@ERROR <> 0
   AND @@TRANCOUNT > 0
    BEGIN
        ROLLBACK;
    END

IF OBJECT_ID(N'tempdb..#tmpErrors') IS NULL
    CREATE TABLE [#tmpErrors] (
        Error INT
    );

IF @@TRANCOUNT = 0
    BEGIN
        INSERT  INTO #tmpErrors (Error)
        VALUES                 (1);
        BEGIN TRANSACTION;
    END


GO
PRINT N'Création de Clé étrangère [dbo].[FK_Histo_Hparam_Sauvegarde_IdSauvegarde]...';


GO
ALTER TABLE [dbo].[Histo_Hparam] WITH NOCHECK
    ADD CONSTRAINT [FK_Histo_Hparam_Sauvegarde_IdSauvegarde] FOREIGN KEY ([IdSauvegarde]) REFERENCES [dbo].[Sauvegarde] ([IdSauvegarde]);


GO
IF @@ERROR <> 0
   AND @@TRANCOUNT > 0
    BEGIN
        ROLLBACK;
    END

IF OBJECT_ID(N'tempdb..#tmpErrors') IS NULL
    CREATE TABLE [#tmpErrors] (
        Error INT
    );

IF @@TRANCOUNT = 0
    BEGIN
        INSERT  INTO #tmpErrors (Error)
        VALUES                 (1);
        BEGIN TRANSACTION;
    END


GO

IF EXISTS (SELECT * FROM #tmpErrors) ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT>0 BEGIN
PRINT N'Succès de la mise à jour de la portion de base de données traitée.'
COMMIT TRANSACTION
END
ELSE PRINT N'Échec de la mise à jour de la portion de base de données traitée.'
GO
IF (SELECT OBJECT_ID('tempdb..#tmpErrors')) IS NOT NULL DROP TABLE #tmpErrors
GO
GO
PRINT N'Vérification de données existantes par rapport aux nouvelles contraintes';


GO
USE [$(DatabaseName)];


GO
ALTER TABLE [dbo].[Histo_Hparam] WITH CHECK CHECK CONSTRAINT [FK_Histo_Hparam_Hyperparamètres_IdHParam];

ALTER TABLE [dbo].[Histo_Hparam] WITH CHECK CHECK CONSTRAINT [FK_Histo_Hparam_Sauvegarde_IdSauvegarde];


GO
PRINT N'Mise à jour terminée.';


GO
