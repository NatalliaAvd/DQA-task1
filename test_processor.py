import glob


class TestProcessor:

    def __init__(self, config, connector, logger):
        self.config = config
        self.connector = connector
        self.logger = logger

    def process(self):
        test_data_files = self.check_test_folder()

        for f in test_data_files:
           self.do_testing(f)

    def check_test_folder(self):
        test_data_folder = self.config.get_test_data_folder()
        return [f for f in glob.glob(test_data_folder + '/*.json', recursive=True)]

    def data_transformation(self, query_results):
        element1 = []
        if len(query_results) == 1:
            transformed_data = query_results[0]
            if len(transformed_data) == 1:
                element = transformed_data[0]
                return element
            elif len(transformed_data) > 1:
                element = list(transformed_data)
                return element
        elif len(query_results) > 1:
            for set in query_results:
                element1.append(list(set))
            return element1
        else:
            return 0

    def do_testing(self, file_name):
        self.logger.start_test(file_name)

        with open(file_name, encoding="utf-8") as f:
            test_data = eval(f.read())

        for test in test_data['tests']:
            self.logger.start_case(test['name'])

            query = test['query']
            expected_result = test['expected']
            actual_result = self.connector.execute(query)

            # transform data from [(), (),..] format
            new_results = self.data_transformation(actual_result)

            if new_results == expected_result:
                self.logger.add_pass(query, new_results)
            else:
                self.logger.add_fail(query, new_results, expected_result)