
import os
from CyberSource.logging.log_configuration import LogConfiguration

class Configuration:
    def __init__(self, organization_id, merchant_id, merchant_secret_id):
        self.authentication_type ="http_signature"
        self.merchantid = organization_id
        self.run_environment = "api.cybersource.com"
        self.request_json_path = ""
        # JWT PARAMETERS
        self.key_alias = organization_id
        self.key_pass = organization_id
        self.key_file_name = organization_id
        self.keys_directory = os.path.join(os.getcwd(), "resources")
        # HTTP PARAMETERS
        self.merchant_keyid = merchant_id
        self.merchant_secretkey = merchant_secret_id
        # META KEY PARAMETERS
        self.use_metakey = False
        self.portfolio_id = ''
        # CONNECTION TIMEOUT PARAMETER
        self.timeout = 1000
        # LOG PARAMETERS
        self.enable_log = True
        self.log_file_name = "cybs"
        self.log_maximum_size = 10487560
        self.log_directory = os.path.join(os.getcwd(), "Logs")
        self.log_level = "Debug"
        self.enable_masking = True
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.log_date_format = "%Y-%m-%d %H:%M:%S"
        self.useMLEGlobally = False

    def get_configuration(self):
        configuration_dictionary = {}
        configuration_dictionary["authentication_type"] = self.authentication_type
        configuration_dictionary["merchantid"] = self.merchantid
        configuration_dictionary["run_environment"] = self.run_environment
        configuration_dictionary["request_json_path"] = self.request_json_path
        configuration_dictionary["key_alias"] = self.key_alias
        configuration_dictionary["key_password"] = self.key_pass
        configuration_dictionary["key_file_name"] = self.key_file_name
        configuration_dictionary["keys_directory"] = self.keys_directory
        configuration_dictionary["merchant_keyid"] = self.merchant_keyid
        configuration_dictionary["merchant_secretkey"] = self.merchant_secretkey
        configuration_dictionary["use_metakey"] = self.use_metakey
        configuration_dictionary["portfolio_id"] = self.portfolio_id
        configuration_dictionary["timeout"] = self.timeout
        configuration_dictionary['useMLEGlobally'] = self.useMLEGlobally

        log_config = LogConfiguration()
        log_config.set_enable_log(self.enable_log)
        log_config.set_log_directory(self.log_directory)
        log_config.set_log_file_name(self.log_file_name)
        log_config.set_log_maximum_size(self.log_maximum_size)
        log_config.set_log_level(self.log_level)
        log_config.set_enable_masking(self.enable_masking)
        log_config.set_log_format(self.log_format)
        log_config.set_log_date_format(self.log_date_format)

        configuration_dictionary["log_config"] = log_config
        return configuration_dictionary
