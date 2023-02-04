import unittest
from unittest.mock import patch
import subprocess
import statistics_of_usage_module as stat

class TestMouduels(unittest.TestCase):

    # Test get_data_as_lines function for "df -h" command
    @patch('subprocess.check_output')
    def test_get_data_as_lines_disks(self, mock_check_output):
        command = ['df', '-h']
        mock_check_output.return_value = self.get_mocked_value_for_disk()

        expected_output = subprocess.check_output(command).decode("utf-8").strip().split("\n")
        result = stat.get_data_as_lines(command)
        
        self.assertEqual(result, expected_output)


    # Test get_data_as_lines function for "free -m" command
    @patch('subprocess.check_output')
    def test_get_data_as_lines_memory(self, mock_check_output):
        command = ['free', '-m']
        mock_check_output.return_value = self.get_mocked_value_for_memory()

        expected_output = subprocess.check_output(command).decode("utf-8").strip().split("\n")
        result = stat.get_data_as_lines(command)
        
        self.assertEqual(result, expected_output)


    # Test get_data_as_lines function for "mpstat -P ALL" command
    @patch('subprocess.check_output')
    def test_get_data_as_lines_cpu(self, mock_check_output):
        command = ["mpstat", "-P","ALL"]
        mock_check_output.return_value = self.get_mocked_value_for_cpu()

        expected_output = subprocess.check_output(command).decode("utf-8").strip().split("\n")
        result = stat.get_data_as_lines(command)
        
        self.assertEqual(result, expected_output)
        
    
    # Test test_data_as_dict function for disks
    @patch('subprocess.check_output')
    def test_data_as_dict_for_disks(self,mock_check_output):
        mock_check_output.return_value = self.get_mocked_value_for_disk()
        
        lines = stat.get_data_as_lines(["df", "-h"])
        headers = lines[0].split()
        
        expected_output = [{'Filesystem': '/dev/sda1', 'Size': '40G', 'Used': '7.7G', 'Avail': '31G', 'Use%': '21%', 'Mounted_on': '/'}]
        result = stat.get_data_as_dict(headers, lines, 1, 'd')
         
        self.assertEqual(result, expected_output)       
        
        
    # Test test_data_as_dict function for memory
    @patch('subprocess.check_output')
    def test_data_as_dict_for_memorys(self,mock_check_output):
        mock_check_output.return_value = self.get_mocked_value_for_memory()
    
        lines = stat.get_data_as_lines(["free", "-m"])
        headers = lines[0].split()
        headers.insert(0, "name")
        
        expected_output = [
            {"name": "Mem:", "total": "3321", "used": "485", "free": "2337", "shared": "11", "buff/cache": "498", "available": "2612"},
            {"name": "Swap:", "total": "8191", "used": "0", "free": "8191"}
        ]
        result = stat.get_data_as_dict(headers, lines, 1, 'm')
        
        self.assertEqual(result, expected_output)
    
    
    # Test test_data_as_dict function for CPU
    @patch('subprocess.check_output')
    def test_data_as_dict_for_cpu(self,mock_check_output):
        mock_check_output.return_value = self.get_mocked_value_for_cpu()
        
        lines = stat.get_data_as_lines(["mpstat", "-P","ALL"])
        headers = lines[2].split()
        headers = headers[2:]
        headers = [name[1:] for name in headers] # to remove % sign from keys names
        headers.insert(0,"CPU")
        
        expected_output = [
            {'CPU': 'all', 'usr': '0.05', 'nice': '0.00', 'sys': '0.05', 'iowait': '0.02', 'irq': '0.00', 'soft': '0.01', 'steal': '0.00', 'guest': '0.00', 'gnice': '0.00', 'idle': '99.87'},
            {'CPU': '0', 'usr': '0.06', 'nice': '0.00', 'sys': '0.05', 'iowait': '0.01', 'irq': '0.00', 'soft': '0.02', 'steal': '0.00', 'guest': '0.00', 'gnice': '0.00', 'idle': '99.85'},
            {'CPU': '1', 'usr': '0.04', 'nice': '0.00', 'sys': '0.05', 'iowait': '0.02', 'irq': '0.00', 'soft': '0.00', 'steal': '0.00', 'guest': '0.00', 'gnice': '0.00', 'idle': '99.89'}
            ]
        result = stat.get_data_as_dict(headers, lines, 3, 'c')
        
        self.assertEqual(result, expected_output)


    # Test get disks usage function
    @patch('subprocess.check_output')
    def test_get_disks_usage(self, mock_check_output):
        mock_check_output.return_value = self.get_mocked_value_for_disk()

        expected_output = [{'Filesystem': '/dev/sda1', 'Size': '40G', 'Used': '7.7G', 'Avail': '31G', 'Use%': '21%', 'Mounted_on': '/'}]
        result = stat.get_disks_usage()

        self.assertEqual(result, expected_output)
        
        
    # Test get memorys usage function
    @patch('subprocess.check_output')
    def test_get_memory_usage(self, mock_check_output):
        mock_check_output.return_value = self.get_mocked_value_for_memory()
        
        expected_output = [
            {"name": "Mem:", "total": "3321", "used": "485", "free": "2337", "shared": "11", "buff/cache": "498", "available": "2612"},
            {"name": "Swap:", "total": "8191", "used": "0", "free": "8191"}
        ]
        result = stat.get_memory_usage()

        self.assertEqual(result, expected_output)


    # Test get CPU usage function
    @patch('subprocess.check_output')
    def test_get_cpu_usage(self, mock_check_output):
        mock_check_output.return_value = self.get_mocked_value_for_cpu()

        expected_output = [
            {'CPU': 'all', 'usr': '0.05', 'nice': '0.00', 'sys': '0.05', 'iowait': '0.02', 'irq': '0.00', 'soft': '0.01', 'steal': '0.00', 'guest': '0.00', 'gnice': '0.00', 'idle': '99.87'},
            {'CPU': '0', 'usr': '0.06', 'nice': '0.00', 'sys': '0.05', 'iowait': '0.01', 'irq': '0.00', 'soft': '0.02', 'steal': '0.00', 'guest': '0.00', 'gnice': '0.00', 'idle': '99.85'},
            {'CPU': '1', 'usr': '0.04', 'nice': '0.00', 'sys': '0.05', 'iowait': '0.02', 'irq': '0.00', 'soft': '0.00', 'steal': '0.00', 'guest': '0.00', 'gnice': '0.00', 'idle': '99.89'}
            ]
        result = stat.get_cpu_usage()

        self.assertEqual(result, expected_output)

    def get_mocked_value_for_disk(self):
        return b'Filesystem Size Used Avail Use% Mounted_on\n/dev/sda1 40G 7.7G 31G 21% /\n'

    def get_mocked_value_for_memory(self):
        return b'total used free shared buff/cache available\nMem: 3321 485 2337 11 498 2612\nSwap: 8191 0 8191\n'

    def get_mocked_value_for_cpu(self):
       return b'Linux 3.10.0-1160.81.1.el7.x86_64 (osboxes.org) 02/01/2023 _x86_64_ (2 CPU)\n \n08:17:15 CPU %usr %nice %sys %iowait %irq %soft %steal %guest %gnice %idle\n08:17:15 all 0.05 0.00 0.05 0.02 0.00 0.01 0.00 0.00 0.00 99.87\n08:17:15 0 0.06 0.00 0.05 0.01 0.00 0.02 0.00 0.00 0.00 99.85\n08:17:15 1 0.04 0.00 0.05 0.02 0.00 0.00 0.00 0.00 0.00 99.89'

if __name__ == '__main__':
    unittest.main()
