===============
Auto-MISCHBARES
===============

.. image:: https://github.com/fuzhanrahmanian/MISCHBARES/blob/main/logo/mischbares_logo.png?raw=true
    :align: center
    :width: 300px


.. image:: https://zenodo.org/badge/546603657.svg
  :target: https://zenodo.org/doi/10.5281/zenodo.10447746
  :align: center

Overview
--------

Auto-MISCHBARES, building upon our `HELAO framework <https://github.com/helgestein/helao-pub>`_,  is designed for high-throughput electrochemical research. It automates the study of different electrolyte and/or electrode materials, different electrochemical protocols in order to characterize the interphase formations at a millimeter scale, enhancing the efficiency of material discovery. This system's significant feature is its ability to autonomously asynchronously orchestrate sequential or parallel experiments, integrated with advanced Quality Control assessments and `MADAP <https://github.com/fuzhanrahmanian/MADAP>`_ for advanced data analysis using AI algorithms. The web interface of Auto-MISCHBARES offers streamlined user control, and its database design adheres to FAIR principles, promoting robust and transparent research in battery material science.



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


Information
-----------

Tutorial and demonstration can be find at `<https://doi.org/10.5281/zenodo.10445749>`_.

The data related to this study is available at `<https://doi.org/10.5281/zenodo.10444324>`_.

Cite this work
--------------

If you use this software in your research, please cite the following paper:


For more detailed information, please visit the `documentation page <https://fuzhanrahmanian.github.io/MISCHBARES>`_
