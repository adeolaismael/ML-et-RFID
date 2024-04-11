CREATE TABLE [dbo].[Histo_Hparam] (
    [IdHisto_HParam] INT IDENTITY(1,1) NOT NULL,
    [IdSauvegarde]  INT           NOT NULL,
    [IdHParam]      INT           NOT NULL,
    [SelectedValue] VARCHAR (255) NOT NULL,
    CONSTRAINT [PK_Histo_Hparam] PRIMARY KEY CLUSTERED ([IdHisto_HParam] ASC),
    CONSTRAINT [FK_Histo_Hparam_Hyperparamètres_IdHParam] FOREIGN KEY ([IdHParam]) REFERENCES [dbo].[Hyperparamètres] ([IdHParam]),
    CONSTRAINT [FK_Histo_Hparam_Sauvegarde_IdSauvegarde] FOREIGN KEY ([IdSauvegarde]) REFERENCES [dbo].[Sauvegarde] ([IdSauvegarde])
);




GO
CREATE NONCLUSTERED INDEX [IX_Histo_Hparam_IdHParam]
    ON [dbo].[Histo_Hparam]([IdHParam] ASC);

