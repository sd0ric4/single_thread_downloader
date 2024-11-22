import unittest
import os
from utils.sender import get_file_list

class TestGetFileList(unittest.TestCase):
    def setUp(self):
        # 创建一个临时目录和一些文件用于测试
        self.test_dir = 'test_images'
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_files = ['file1.jpg', 'file2.jpg', 'file3.jpg']
        for file_name in self.test_files:
            with open(os.path.join(self.test_dir, file_name), 'w') as f:
                f.write('test content')

    def tearDown(self):
        # 删除测试目录和文件
        for file_name in self.test_files:
            os.remove(os.path.join(self.test_dir, file_name))
        os.rmdir(self.test_dir)

    def test_get_file_list(self):
        # 测试 get_file_list 函数
        file_list = get_file_list(self.test_dir)
        print(file_list)
        self.assertEqual(sorted(file_list), sorted(self.test_files))

if __name__ == '__main__':
    unittest.main()