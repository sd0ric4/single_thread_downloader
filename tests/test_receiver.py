import unittest
import threading
from utils.sender import start_server
from utils.receiver import test_connection, download_file
import os

class TestReceiver(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 启动服务器线程
        cls.server_thread = threading.Thread(target=start_server, args=('localhost', 12345), daemon=True)
        cls.server_thread.start()

    def test_test_connection_success(self) -> None:
        # 调用 test_connection 函数
        message, update = test_connection('localhost', 12345)
        # 断言
        self.assertIn("连接成功", message)
        self.assertGreater(len(update['choices']), 0)  # 假设服务器目录中有文件
    
    def test_test_connection_failure(self) -> None:
        # 调用 test_connection 函数，使用错误的端口
        message, update = test_connection('localhost', 55555)
        # 断言
        self.assertIn("连接失败", message)
        self.assertEqual(update['choices'], [])
    
    def test_download_file(self) -> None:

        # 调用 download_file 函数
        file_path = download_file('downloaded.jpg', file_path='./Downloads', host='localhost', port=12345)
        
        # 断言
        self.assertTrue(os.path.exists(file_path))
    
if __name__ == '__main__':
    unittest.main()