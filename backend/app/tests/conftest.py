import os
import tempfile

# 必须在导入任何 app.* 之前指定独立测试库
os.environ.setdefault("DATA_DIR", tempfile.mkdtemp(prefix="giftwrap-test-"))
