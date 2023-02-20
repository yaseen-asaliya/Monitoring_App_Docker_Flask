import sys
sys.path.insert(0, '/root/flask_monitoring_app')
import database_configrations as dbc
import unittest
from unittest.mock import Mock, patch

class TestMonitoringAppDatabase(unittest.TestCase):

    def setUp(self):
        self.mock_cursor = Mock()
        self.mock_conn = Mock()
        self.mock_conn.cursor.return_value = self.mock_cursor

        self.database = dbc.MonitoringAppDatabase()
        self.database.cur = self.mock_cursor
        self.database.conn = self.mock_conn

    def test_init(self):
        self.assertIsNotNone(self.database.conn)
        self.assertIsNotNone(self.database.cur)

    def test_setup_database_tables(self):
        self.database.setup_database_tables()

        self.mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS disk (time TIMESTAMP, disk_name TEXT, size TEXT, used TEXT, Avail TEXT, Use TEXT, Mount_on TEXT);")
        self.mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS memory (time TIMESTAMP, name TEXT, total INTEGER, used INTEGER, free INTEGER, shared INTEGER, buff INTEGER, available INTEGER);")
        self.mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS cpu (time TIMESTAMP, cpu_name TEXT, usr FLOAT, nice FLOAT, sys FLOAT, iowait FLOAT, irq FLOAT, soft FLOAT, steal FLOAT, guest FLOAT, gnice FLOAT, idle FLOAT);")
        self.mock_conn.commit.assert_called_once()

    @patch('subprocess.check_output')
    def test_set_disks_usage_in_db(self, mock_check_output):
        mock_check_output.return_value = self.get_mocked_value_for_disk()

        self.database.set_disks_usage_in_db()
        self.mock_conn.commit.assert_called_once()

    @patch('subprocess.check_output')
    def test_set_memory_usage_in_db(self, mock_check_output):
        mock_check_output.return_value = self.get_mocked_value_for_memory()

        self.database.set_memory_usage_in_db()
        self.mock_conn.commit.assert_called_once()

    @patch('subprocess.check_output')
    def test_set_cpu_usage_in_db(self, mock_check_output):
        mock_check_output.return_value = self.get_mocked_value_for_cpu()

        self.database.set_cpu_usage_in_db()
        self.mock_conn.commit.assert_called_once()

    @patch('subprocess.check_output')
    def test_set_and_collect_data_in_database(self, mock_check_output):
        mock_check_output_disk = Mock()
        mock_check_output_disk.return_value = self.get_mocked_value_for_disk()
        mock_check_output.side_effect = [mock_check_output_disk.return_value,
                                         self.get_mocked_value_for_memory(),
                                         self.get_mocked_value_for_cpu()]

        self.database.set_and_collect_data_in_database()
        self.assertEqual(self.mock_conn.commit.call_count, 3)

    def test_close_connection(self):
        self.database.close_conncetion()
        self.mock_conn.close.assert_called_once()

    def test_refresh_database(self):
        self.mock_cursor.fetchall.return_value = [('disk',), ('memory',),('cpu',)]
        self.database.refresh_database()

        self.mock_conn.commit.assert_called_once()

    def test_get_usage_from_db(self):
        disks_result = self.database.get_usage_from_db('disk')
        memory_result = self.database.get_usage_from_db('memory')
        cpu_result = self.database.get_usage_from_db('cpu')

        self.assertTrue(len(disks_result) != 0 and len(memory_result) != 0 and len(cpu_result) != 0)

    def get_mocked_value_for_disk(self):
        return b'Filesystem Size Used Avail Use% Mounted\n/dev/sda1 40G 7.7G 31G 21% /\n'

    def get_mocked_value_for_memory(self):
        return b'total used free shared buff/cache available\nMem: 3321 485 2337 11 498 2612\nSwap: 8191 0 8191\n'

    def get_mocked_value_for_cpu(self):
       return b'Linux 3.10.0-1160.81.1.el7.x86_64 (osboxes.org) 02/01/2023 _x86_64_ (2 CPU)\n \n08:17:15 CPU %usr %nice %sys %iowait %irq %soft %steal %guest %gnice %idle\n08:17:15 all 0.05 0.00 0.05 0.02 0.00 0.01 0.00 0.00 0.00 99.87\n08:17:15 0 0.06 0.00 0.05 0.01 0.00 0.02 0.00 0.00 0.00 99.85\n08:17:15 1 0.04 0.00 0.05 0.02 0.00 0.00 0.00 0.00 0.00 99.89'

if __name__ == '__main__':
    unittest.main()

