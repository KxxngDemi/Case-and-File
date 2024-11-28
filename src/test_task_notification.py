import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from task_notification import TaskNotification


class TestTaskNotification(unittest.TestCase):
    
    @patch('sqlite3.connect')
    def test_get_tasks_due(self, mock_connect):
        
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Task 1',), ('Task 2',)]
        
        reminder = TaskNotification()
        date = datetime.now().date()
        tasks = reminder.get_tasks_due(date)
       
      
        self.assertEqual(tasks, ['Task 1', 'Task 2'])
        mock_connect.return_value.close.assert_called_once()

    
    @patch('schedule.run_pending')
    @patch('time.sleep')
    def test_run_scheduler(self, mock_sleep, mock_run_pending):
        reminder = TaskNotification()
        
        
        with patch('builtins.print') as mock_print:
            reminder.run_scheduler()
           
      
            mock_print.assert_any_call("Task email scheduler is running...")
        
            mock_run_pending.assert_called()
            mock_sleep.assert_called()
        
if __name__ == '__main__':
    unittest.main()
