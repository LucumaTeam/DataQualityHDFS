class TestService:

    def assert_tests(interface):

        tables = interface.tables

        if (len(tables) > 0):
            for table in tables:
                table.tests.assert_test()
