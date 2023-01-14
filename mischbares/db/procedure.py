
from mischbares.db.measurement import Measurements
from mischbares.config.main_config import config
from mischbares.logger import logger

log = logger.get_logger("db_procedure")

class Procedure(Measurements):
    """class for handling procedures database tables"""
    def __init__(self):
        super().__init__()
        self.procedure_id = None
        #TODO add procedures when the tables are created
        # Define a dictionary that maps procedure names to tuples containing the SQL query and the number of values
        self.query_dict_information = {
        "ocp": ("INSERT INTO ocp_procedure (procedure_id, duration, interval_time, ocp_potential, ocp_measurment_id) VALUES \
                (nextval('ocp_procedure_procedure_id_seq'::regclass), %s, %s, %s, %s)", 4),
        "cv": ("---", 5),
        "ca": ("---", 5),
        "cp": ("---", 5),
        "eis": ("---", 5),
        "lissajous": ("---", 5),
        }

        # Dictionary that maps procedure names to tuples containing the SQL query and the number of values
        self.query_raw_data_information = {
            "ocp": ("INSERT INTO ocp_raw (current, corrected_time, index, potential, dpotential_dt,\
                    power, charge, dpower_dt, dcharge_dt, procedure_id) VALUES", 9),
            "cv": ("---", 5),
            "ca": ("---", 5),
            "cp": ("---", 5),
            "eis": ("---", 5),
            "lissajous": ("---", 5),
        }

    def add_procedure_information(self, *args):
        """add procedure information to the database

        Args:
            *args: The values to be inserted into the database
        """
        # Look up the relevant SQL query and number of values based on the procedure name
        query, num_values = self.query_dict_information.get(self.procedure_name, (None, None))
        if query and len(args) == num_values:
            # Execute the query. The first two arguments are the procedure name and the procedure id
            # The rest of the arguments are the values to be inserted
            # The procedure name is used to determine the table name
            # Args is a tuple so it can be added to the existing tuple containing the procedure name and id
            commit_status = self.commit(query, args)
            if commit_status:
                self.procedure_id = int(self.execute(f"SELECT currval('{self.procedure_name}_procedure_procedure_id_seq'::regclass)").iloc[0][0])
                log.info(f"Procedure {self.procedure_name} information added.")
        else:
            commit_status = False
            log.error("Invalid number of arguments for procedure")
        return commit_status

    def get_procedure_information(self, procedure):
        """get procedure information from the database

        Args:
            procedure (str): name of the procedure
        """
        procedure_dict_information = {
            "ocp": ("SELECT * FROM ocp_procedure WHERE procedure_id = %s"),
            "cv": ("SELECT * FROM cv_procedure WHERE procedure_id = %s"),
            "ca": ("SELECT * FROM ca_procedure WHERE procedure_id = %s"),
            "cp": ("SELECT * FROM cp_procedure WHERE procedure_id = %s"),
            "eis": ("SELECT * FROM eis_procedure WHERE procedure_id = %s"),
            "lissajous": ("SELECT * FROM lissajous_procedure WHERE procedure_id = %s"),
        }
        sql = procedure_dict_information.get(procedure, None)
        proc_info = self.execute(sql, (self.procedure_id, ))
        return proc_info

    def add_raw_procedure_data(self, data):
        """add procedure data to the database

        Args:
            data (dict): dictionary containing the data to be added
        """
        # Prepare the dataset
        data.pop("Time")
        tuples = [tuple(data[col]) for col in data.keys()]
        # Look up the relevant SQL query and number of values based on the procedure name
        query, num_values = self.query_raw_data_information.get(self.procedure_name, (None, None))
        if query and len(tuples) == num_values:
            # Create a string of placeholder values to be inserted
            s = "("+",".join(["%s"] *(len(tuples)+1))+")"
            # User mogrify to get the query with the values inserted
            transposed_tuples = list(zip(*tuples))
            # Add the procedure id to the end of every tuple of transposed_tuples
            data_tuples = [tup + (self.procedure_id, ) for tup in transposed_tuples]
            # Assemble the argument string for the query
            args_str = ",".join(self.cursor.mogrify(s, tup).decode("utf-8") for tup in data_tuples)
            #query = query + ",".join(values)
            commit_status = self.commit(query+args_str)
        else:
            commit_status = False
            log.error("Invalid number of arguments for procedure")
        return commit_status


    def get_raw_data_by_procedure(self, procedure):
        """get raw data from the database given a procedure name

        Args:
            procedure (str): name of the procedure
        """
        procedure_dict_raw_data = {
            "ocp": ("SELECT * FROM ocp_raw WHERE procedure_id = %s"),
            "cv": ("SELECT * FROM cv_raw WHERE procedure_id = %s"),
            "ca": ("SELECT * FROM ca_raw WHERE procedure_id = %s"),
            "cp": ("SELECT * FROM cp_raw WHERE procedure_id = %s"),
            "eis": ("SELECT * FROM eis_raw WHERE procedure_id = %s"),
            "lissajous": ("SELECT * FROM lissajous_raw WHERE procedure_id = %s"),
        }
        sql = procedure_dict_raw_data.get(procedure, None)
        raw_data = self.execute(sql, (self.procedure_id, ))
        return raw_data

