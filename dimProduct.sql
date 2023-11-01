/****** Object: Table [dbo].[dimProduct] Script Date: 9/29/2023 11:46:59 PM ******/

-- Drop the table if it exists
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[dimProduct]') AND type = N'U')
    DROP TABLE [dbo].[dimProduct];
GO

-- Set ANSI_NULLS and QUOTED_IDENTIFIER options
SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

-- Create the dimProduct table
CREATE TABLE [dbo].[dimProduct](
    [Product_ID] [int] IDENTITY(1,1),
    [Name] [nvarchar](255) NULL,
    [Brand] [nvarchar](50) NULL,
    [Screen_Size] [nvarchar](2) NULL,
    [Customer_Rating] [float] NULL,
    [Number_of_Customer_Reviews] [float] NULL,
    [Last_Update] datetime
) ON [PRIMARY];
GO

-- Create a trigger to update Last_Update on UPDATE operations
CREATE TRIGGER trigger_dimProduct_change_lastupdatedby
ON dbo.[dimProduct]
AFTER UPDATE
AS
BEGIN
    UPDATE dp
    SET dp.Last_Update = CURRENT_TIMESTAMP
    FROM dbo.[dimProduct] dp
    JOIN INSERTED i ON dp.Product_ID = i.Product_ID;
END;
GO

-- Populate Values in the table
SELECT
    [Name],
    SUBSTRING([Name], PATINDEX('%[0-9][0-9]%', [Name]), 2) AS Screen_Size,
    CASE
        WHEN CHARINDEX('OLED', [Name]) <> 0 THEN 'OLED'
        WHEN CHARINDEX('QLED', [Name]) <> 0 THEN 'QLED'
        WHEN CHARINDEX('QNED', [Name]) <> 0 THEN 'QNED'
        WHEN CHARINDEX('ULED', [Name]) <> 0 THEN 'ULED'
        ELSE 'LED'
    END AS Panel_Type,
    CASE
        WHEN [Name] LIKE '%SMART%' THEN 'Y'
        ELSE 'N'
    END AS SMART_TV,
    CASE
        WHEN [Name] LIKE '%Google%' THEN 'Google'
        WHEN [Name] LIKE '%Fire%' THEN 'Fire'
        WHEN [Name] LIKE '%Roku%' THEN 'Roku'
        WHEN [Name] LIKE '%webOS%' THEN 'webOS'
        WHEN [Name] LIKE '%Tizen%' THEN 'Tizen'
        WHEN [Name] LIKE '%Android%' THEN 'Android'
        ELSE 'Others'
    END AS OS,
    [Sales_Price],
    [Regular_Price],
    [Customer_Rating],
    [Number_of_Customer_Reviews],
    [Brand]
INTO #TEMP_INSERT
FROM [dbo].[best_buy_all_cleaned]
ORDER BY [Name];

-- Insert data from #TEMP_INSERT into dimProduct table
INSERT INTO [dbo].[dimProduct] (
    [Name],
    [Brand],
    [Screen_Size],
    [Customer_Rating],
    [Number_of_Customer_Reviews],
    [Last_Update]
)
SELECT
    [Name],
    [Brand],
    [Screen_Size],
    [Customer_Rating],
    [Number_of_Customer_Reviews],
    GETDATE() -- Use GETDATE() to set the Last_Update column
FROM #TEMP_INSERT;

-- Drop the temporary table
DROP TABLE #TEMP_INSERT;
