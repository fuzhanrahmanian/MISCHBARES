===============
Auto-MISCHBARES
===============

.. image:: logo/mischbares_logo.png
    :align: center
    :width: 300px

Overview
--------

Auto-MISCHBARES, building upon our `HELAO framework <https://github.com/helgestein/helao-pub>`_, is designed for high-throughput electrochemical research. It automates the study different electrolyte and/or electrode materials, different electrochemcial protocols in order to characterize the interphase formations at a millimeter scale, enhancing the efficiency of material discovery. This system's significant feature is its ability to autonoumussly asynchronously orchestrate sequential or parallel experiments, integrated with advanced Quality Control assessments and `MADAP <https://github.com/fuzhanrahmanian/MADAP>`_ for advanced data analysis using AI algorithms. The web interface of Auto-MISCHBARES offers streamlined user control, and its database design adheres to FAIR principles, promoting robust and transparent research in battery material science.



Installation
------------

Requirements
~~~~~~~~~~~~

- Python 3.8
- PostgreSQL
- Libraries listed in `requirements.txt`

Installation Steps
~~~~~~~~~~~~~~~~~~

1. Clone the repository::

     git clone https://github.com/fuzhanrahmanian/MISCHBARES.git

2. Navigate to the directory::

     cd MISCHBARES

3. Install the required libraries::

     pip install -r requirements.txt

Starting the Application
------------------------

Run the application::

    python app.py

Database Setup
--------------

1. Navigate to the `db` directory::

     cd db

2. Initialize the PostgreSQL database using the schema file::

     psql -U [username] -d [database_name] -a -f mischbares_db.sql

Replace `[username]` and `[database_name]` with your PostgreSQL credentials.

Cite this work
--------------

If you use this software in your research, please cite the following paper:


For more detailed information, please visit the documentation page: https://fuzhanrahmanian.github.io/MISCHBARES/