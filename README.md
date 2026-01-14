
🥛 Milk Centre Diary Management System

Project Overview

The Milk Centre Diary Management System is a real-world, production-ready web application designed to digitize daily milk collection and farmer billing operations in a dairy milk centre.
This system replaces traditional manual diary books with a secure, accurate, and automated digital solution.

The application is built as a single-file Streamlit app integrated with a MySQL database, making it easy to run, deploy, and maintain. It ensures data integrity, supports transparent farmer billing, and automates 15-day billing cycles, which are commonly followed in dairy centres.



Problem Statement

Traditional milk centres maintain daily milk records manually using paper diaries, which leads to:

Human calculation errors

Duplicate or missing entries

Difficulty in generating reports

Time-consuming 15-day billing calculations

Lack of transparency for farmers


This project solves these problems by providing a digital diary system with automatic calculations, reporting, and billing.




Key Objectives

Digitize daily milk collection records

Prevent duplicate milk entries (Morning/Evening only once per day)

Automate milk payment calculation

Generate daily, period-wise, and farmer-wise reports

Automate 15-day billing cycles

Provide downloadable PDF bills

Notify farmers about billing via SMS





Core Features

👨‍🌾 Farmer Management

Register farmers with name, mobile number, and village

Maintain a centralized farmer database





📒 Daily Milk Diary Entry

Milk collection recorded twice per day only:

Morning

Evening


System prevents duplicate session entries for the same farmer on the same day

Each entry records:

Date

Session (Morning / Evening)

Milk quantity (liters)

Fat percentage





🧮 Automatic Payment Calculation

Payment is calculated using a fixed-rate dairy formula:

Amount = Quantity × Fat × Constant Rate

Eliminates manual calculation errors

Ensures consistency and transparency





📊 Reports Module

Daily Report

Farmer-wise milk collection

Session-wise entries

Total earnings per day


Date-Range Report

Custom period selection

Farmer-wise total amount

Overall earnings summary


Reports are displayed in tabular and graphical format for easy understanding.




🧾 Automated 15-Day Billing System

Supports standard dairy billing cycles:

1st – 15th

16th – End of Month


Automatically aggregates:

Total milk supplied per farmer

Total payable amount


No manual billing calculations required





📄 Individual Farmer PDF Bill

Generates individual farmer bills in PDF format

Bill includes:

Farmer name

Billing period

Total milk supplied

Total amount payable


Bills can be downloaded and shared easily



Data Integrity & Validation

Prevents duplicate milk collection entries:

Only one Morning and one Evening entry per farmer per day


Database-level UNIQUE constraint ensures data consistency

Application-level validation provides user-friendly error messages



Technology Stack

Layer	Technology

Frontend & Logic	Streamlit
Database	MySQL
Data Processing	Pandas
PDF Generation	ReportLab


How to Run the Project

streamlit run app.py

> The application runs as a single Streamlit file, making it simple to execute and deploy.


Future Enhancements

WhatsApp bill notifications

Role-based access (Admin / Staff)

Farmer login portal

Monthly analytics dashboard

Integration with digital payment gateways


Conclusion

The Milk Centre Diary Management System provides a reliable, scalable, and transparent solution for managing dairy operations. By automating daily entries, billing cycles, reporting, and notifications, the system significantly improves efficiency and trust between milk centres and farmers.


