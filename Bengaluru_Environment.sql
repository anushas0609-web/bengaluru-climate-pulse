-- =========================================================================
-- PROJECT: Bengaluru Climate Pulse (Production-Grade Database Setup)
-- DESCRIPTION: Fresh backend setup for weather, AQI, and water data.
-- =========================================================================

-- 1. Create Database and Set Context
CREATE DATABASE IF NOT EXISTS Bengaluru_Environment;
USE Bengaluru_Environment;

-- 2. Drop Existing Tables to guarantee a fresh, duplicate-free state
DROP TABLE IF EXISTS Live_Environment_Data;
DROP TABLE IF EXISTS Historical_Environment_Data;
DROP TABLE IF EXISTS Reservoir_Levels;
DROP TABLE IF EXISTS Historical_Water_Data;

-- =========================================================================
-- TABLE 1: Live Environment Data (Populated by Python API script)
-- =========================================================================
CREATE TABLE Live_Environment_Data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    temperature_c FLOAT NOT NULL,
    humidity_percent INT NOT NULL,
    aqi INT NOT NULL
);

-- =========================================================================
-- TABLE 2: Historical Environment Data (Populated by Python API script)
-- =========================================================================
CREATE TABLE Historical_Environment_Data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    record_date DATE UNIQUE NOT NULL, -- UNIQUE prevents duplicate dates
    max_temp_c FLOAT NOT NULL,
    min_temp_c FLOAT NOT NULL,
    max_aqi INT,
    min_aqi INT
);

-- =========================================================================
-- TABLE 3: Current Reservoir Levels (Static Data)
-- =========================================================================
CREATE TABLE Reservoir_Levels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservoir_name VARCHAR(50) UNIQUE NOT NULL, -- UNIQUE prevents duplicate names
    current_level_tmc FLOAT NOT NULL,
    full_capacity_tmc FLOAT NOT NULL,
    last_updated DATE NOT NULL
);

-- Insert the real data (UNIQUE constraint guarantees it only happens once)
INSERT INTO Reservoir_Levels (reservoir_name, current_level_tmc, full_capacity_tmc, last_updated) VALUES 
('KRS (Krishna Raja Sagara)', 26.35, 49.45, '2026-10-27'),
('Kabini', 13.43, 19.52, '2026-10-27'),
('Hemavathi', 17.40, 37.10, '2026-10-27'),
('Harangi', 5.37, 8.50, '2026-10-27');

-- =========================================================================
-- TABLE 4: Historical Water Data (Static Data for Bar Chart)
-- =========================================================================
CREATE TABLE Historical_Water_Data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    record_month VARCHAR(20) UNIQUE NOT NULL, -- UNIQUE prevents duplicate months
    total_water_tmc FLOAT NOT NULL
);

-- Insert the 2026 monthly trend data
INSERT INTO Historical_Water_Data (record_month, total_water_tmc) VALUES 
('Jan 2026', 80.5),
('Feb 2026', 75.2),
('Mar 2026', 68.0),
('Apr 2026', 60.5),
('May 2026', 55.2),
('Jun 2026', 58.0),
('Jul 2026', 65.5),
('Aug 2026', 72.0),
('Sep 2026', 78.5),
('Oct 2026', 62.5);

-- =========================================================================
-- VERIFICATION QUERIES
-- Run these to ensure the data is perfectly clean.
-- =========================================================================
SELECT '--- Reservoir Levels (Should be exactly 4 rows) ---' AS Status;
SELECT * FROM Reservoir_Levels;

SELECT '--- Historical Water Data (Should be exactly 10 rows) ---' AS Status;
SELECT * FROM Historical_Water_Data;