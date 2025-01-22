CREATE TABLE SYSTEMS (
    system_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each system
    system_name TEXT NOT NULL,                    -- Name of the system (e.g., LoanEngine, DerivativeDesk)
    description TEXT                              -- Description of the system
);

-- Insert sample systems
INSERT INTO SYSTEMS (system_name, description)
VALUES
('LoanEngine', 'Transaction system for booking and managing loans.'),
('DerivativeDesk', 'Transaction system for booking and managing derivatives.'),
('SFTTracker', 'Transaction system for booking and managing Securities Financing Transactions (SFTs).'),
('CPCentral', 'Reference system for managing counterparty data.'),
('RDS', 'Reference system for maintaining product and collateral data.'),
('ExposureEngine', 'System for calculating Exposure at Default (EAD).'),
('RWACore', 'System for calculating Risk-Weighted Assets (RWA).'),
('DataHub', 'Aggregator system for consolidating data across dimensions.'),
('ReportSuite', 'System for generating regulatory and internal management reports.');


CREATE TABLE ATTRIBUTES (
    attribute_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each attribute
    attribute_name TEXT NOT NULL,                               -- Name of the attribute (e.g., Transaction_ID, EAD, etc.)
    description TEXT,                                 -- Description of the attribute
    owner TEXT,                                       -- Owner of the attribute (e.g., Risk Team, Transaction Team)
    origin_system TEXT,                               -- The system where the attribute originates (e.g., LoanEngine, EADCalc)
    value_data_type TEXT,                             -- The data type of the attribute (e.g., String, Decimal)
    UNIQUE(attribute_name)                                      -- Ensure no duplicate attribute names
);

-- Insert attributes with updated origin systems and changed Boolean to String
INSERT INTO ATTRIBUTES (attribute_name, description, owner, origin_system, value_data_type)
VALUES
('Transaction_ID', 'Unique identifier for each transaction or trade.', 'Transaction Team', 'LoanEngine,DerivativeDesk,SFTTracker', 'String'),
('Counterparty_ID', 'Unique identifier for the counterparty involved in the transaction.', 'Reference Data Team', 'CPCentral,RDS', 'String'),
('Exposure_Amount', 'Nominal value or exposure amount of a transaction.', 'Transaction Team', 'LoanEngine,DerivativeDesk,SFTTracker', 'Decimal'),
('Collateral_Value', 'Value of collateral posted for a transaction.', 'Risk Team', 'RDS', 'Decimal'),
('Currency', 'Currency in which the transaction is denominated.', 'Transaction Team', 'LoanEngine,DerivativeDesk,SFTTracker', 'String'),
('MPOR', 'Margin Period of Risk for the transaction.', 'Risk Team', 'LoanEngine,DerivativeDesk,SFTTracker', 'Integer'),
('Netting_Agreement_ID', 'Identifier for the netting agreement associated with the transaction.', 'Risk Team', 'LoanEngine,DerivativeDesk,SFTTracker', 'String'),
('Booking_Date', 'Date when the transaction was booked.', 'Transaction Team', 'LoanEngine,DerivativeDesk,SFTTracker', 'Date'),
('Settlement_Date', 'Date when the transaction settles.', 'Transaction Team', 'LoanEngine,DerivativeDesk,SFTTracker', 'Date'),
('Maturity_Date', 'Date when the transaction matures.', 'Transaction Team', 'LoanEngine,DerivativeDesk,SFTTracker', 'Date'),
('EAD', 'Calculated exposure at default value for a transaction.', 'Risk Team', 'ExposureEngine', 'Decimal'),
('EPE', 'Expected Positive Exposure for a transaction.', 'Risk Team', 'ExposureEngine', 'Decimal'),
('PFE', 'Potential Future Exposure for a transaction.', 'Risk Team', 'ExposureEngine', 'Decimal'),
('PD', 'Probability of Default for the counterparty.', 'Risk Team', 'RDS', 'Decimal'),
('LGD', 'Loss Given Default for the transaction.', 'Risk Team', 'RWACore', 'Decimal'),
('RWA', 'Risk-Weighted Asset value calculated based on EAD, PD, and LGD.', 'Risk Team', 'RWACore', 'Decimal'),
('Risk_Weight', 'Regulatory risk weight assigned to a transaction based on product and counterparty risk.', 'Risk Team', 'RWACore', 'Decimal'),
('Regulatory_Capital', 'Amount of capital required under regulatory rules for a transaction or portfolio.', 'Risk Team', 'RWACore', 'Decimal'),
('COB_Date', 'Close of Business date for reporting purposes.', 'Reporting Team', 'ReportSuite', 'Date'),
('Region_Code', 'Geographical code for the counterparty or transaction region.', 'Reference Data Team', 'CPCentral,RDS', 'String'),
('SWWR_Flag', 'Indicates if the transaction is under a worst-case scenario analysis.', 'Risk Team', 'ExposureEngine', 'String'),
('Stress_Scenario', 'Specific stress test scenario applied to the transaction.', 'Stress Testing Team', 'ExposureEngine', 'String'),
('Netting_Set_ID', 'Identifier for the netting set associated with the transaction.', 'Risk Team', 'ExposureEngine', 'String'),
('Counterparty_Name', 'Name of the counterparty involved in the transaction.', 'Reference Data Team', 'CPCentral', 'String');


CREATE TABLE ATTRIBUTE_SYSTEM_MAPPING (
    attribute_id INTEGER NOT NULL,           -- Foreign key referencing attribute_id from ATTRIBUTES
    system_id INTEGER NOT NULL,              -- Foreign key referencing system_id from SYSTEMS
    system_attribute_name TEXT NOT NULL,     -- The name of the attribute in the specific system
    PRIMARY KEY (attribute_id, system_id),   -- Composite primary key for attribute-system combination
    FOREIGN KEY (attribute_id) REFERENCES ATTRIBUTES(attribute_id),
    FOREIGN KEY (system_id) REFERENCES SYSTEMS(system_id)
);


INSERT INTO ATTRIBUTE_SYSTEM_MAPPING (attribute_id, system_id, system_attribute_name)
VALUES 
(1, 1, 'TXN_ID'), 
(1, 2, 'Txn_ID'),
(1, 3, 'Trans_ID'),
(1, 4, 'Transaction_ID'),
(1, 5, 'Transaction_ID'),
(1, 6, 'Txn_Id'),
(1, 7, 'TxnRef'),
(1, 8, 'Transaction_Identifier'),
(2, 1, 'Counterparty_ID'),
(2, 2, 'Counterparty_Ref'),
(2, 3, 'CP_ID'),
(2, 4, 'Counterparty_Code'),
(2, 5, 'Counterparty_Code'),
(2, 6, 'Counterparty_ID'),
(2, 7, 'CP_ID'),
(2, 8, 'CP_Reference'),
(3, 1, 'Exposure_Amount'),
(3, 2, 'Exposure_Value'),
(3, 3, 'Exposed_Value'),
(3, 4, 'Exposure_Amount'),
(3, 5, 'Exposure_Amount'),
(3, 6, 'Exposure_Value'),
(3, 7, 'Exposure_Amount'),
(3, 8, 'Exposure_Value'),
(4, 1, 'Collateral_Value'),
(4, 2, 'Collateral_Amount'),
(4, 3, 'Collateral_Value'),
(4, 4, 'Collateral_Amount'),
(4, 5, 'Collateral_Value'),
(4, 6, 'Collateral_Value'),
(4, 7, 'Collateral_Value'),
(4, 8, 'Collateral_Amount'),
(5, 1, 'Currency_Code'),
(5, 2, 'Transaction_Currency'),
(5, 3, 'Currency_Type'),
(5, 4, 'Currency'),
(5, 5, 'Currency_Type'),
(5, 6, 'Transaction_Currency'),
(5, 7, 'Currency_Code'),
(5, 8, 'Currency_Unit'),
(6, 1, 'MPOR'),
(6, 2, 'MPOR_Value'),
(6, 3, 'Margin_Period_Risk'),
(6, 6, 'Margin_Period_of_Risk'),
(6, 7, 'MPOR_Interval'),
(6, 8, 'Risk_Period'),
(7, 1, 'Netting_Agreement_ID'),
(7, 2, 'Netting_Contract_ID'),
(7, 3, 'Netting_Agreement_Reference'),
(7, 6, 'Netting_Agreement_ID'),
(7, 7, 'Netting_ID'),
(7, 8, 'Agreement_ID'),
(8, 1, 'Booking_Date'),
(8, 2, 'Txn_Booking_Date'),
(8, 3, 'Transaction_Book_Date'),
(8, 6, 'Booking_Date'),
(8, 7, 'Transaction_Booking_Date'),
(8, 8, 'Trade_Date'),
(9, 1, 'Settlement_Date'),
(9, 2, 'Settle_Date'),
(9, 3, 'Settlement_Date'),
(9, 6, 'Settlement_Date'),
(9, 7, 'Settle_Date'),
(9, 8, 'Settlement_Deadline'),
(10, 1, 'Maturity_Date'),
(10, 2, 'Maturity_Date'),
(10, 3, 'Maturity_Expiry'),
(10, 6, 'Maturity_Date'),
(10, 7, 'Expiry_Date'),
(10, 8, 'Maturity_Term'),
(11, 6, 'EAD_Value'),
(11, 7, 'Exposure_at_Default'),
(11, 8, 'EAD_Amount'),
(12, 6, 'EPE_Value'),
(12, 7, 'Positive_Exposure'),
(12, 8, 'EPE_Amount'),
(13, 6, 'PFE_Value'),
(13, 7, 'Potential_Exposure'),
(13, 8, 'PFE_Amount'),
(14, 6, 'SWWR_Flag'),
(14, 7, 'Sovereign_Risk_Flag'),
(14, 8, 'Single_Entity_Risk_Flag'),
(15, 6, 'Stress_Scenario'),
(15, 7, 'Stress_Test_Scenario'),
(15, 8, 'Stress_Scenario_Type'),
(16, 6, 'Netting_Set_ID'),
(16, 7, 'Netting_Set_Identifier'),
(16, 8, 'Netting_Set_ID'),
(17, 4, 'Counterparty_Name'),
(17, 1, 'CP_Name'),
(17, 2, 'CP_Name'),
(17, 3, 'Counterparty_Description'),
(17, 6, 'Counterparty_Name'),
(17, 7, 'Counterparty_Entity'),
(18, 4, 'Region_Code'),
(18, 6, 'Region_Code'),
(18, 7, 'Region_ID'),
(19, 5, 'Probability_of_Default'),
(19, 6, 'PD_Value'),
(19, 7, 'PD_Rating');
