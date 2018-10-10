import unittest

import zstandard as zstd

class TestTwoFrame(unittest.TestCase):
    def test_read_lines_read_to_iter(self):
        with open("two_frame.zst", "rb") as fh:
            dctx = zstd.ZstdDecompressor()
            i = dctx.read_to_iter(fh)
            first_line = next(i)
            self.assertEqual(first_line, "first line\n")
            second_line = next(i)
            self.assertEqual(first_line, "second line\n")

    def test_read_lines_decompress(self):
        with open("two_frame.zst", "rb") as fh:
            dctx = zstd.ZstdDecompressor()
            contents = dctx.decompress(fh.read(), max_output_size=1024*1024*50)
            self.assertEqual(contents, "first line\nsecond line\n")

    def test_stream_reader(self):
        with open("two_frame.zst", "rb") as fh:
            dctx = zstd.ZstdDecompressor()
            contents = ""
            with dctx.stream_reader(fh) as reader:
                contents = reader.read(16384)
            self.assertEqual(contents, "first line\nsecond line\n")
