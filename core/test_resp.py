from core.resp import readLength, readBulkString, readSimpleString, readArray

class TestReadLength:

    def test_single_digit(self):
        value, delta, err = readLength(b"6\r\nyellow\r\n")
        assert value == 6
        assert delta == 3
        assert err is None

    def test_multi_digit(self):
        value, delta, err = readLength(b"12\r\nhelloworld!!\r\n")
        assert value == 12
        assert delta == 4
        assert err is None

    def test_zero_length(self):
        value, delta, err = readLength(b"0\r\n\r\n")
        assert value == 0
        assert delta == 3
        assert err is None


class TestReadBulkString:

    def test_simple(self):
        value, consumed, err = readBulkString(b"$6\r\nyellow\r\n")
        assert value == "yellow"
        assert consumed == 12
        assert err is None

    def test_empty_string(self):
        value, consumed, err = readBulkString(b"$0\r\n\r\n")
        assert value == ""
        assert consumed == 6
        assert err is None

    def test_string_with_spaces(self):
        value, consumed, err = readBulkString(b"$5\r\nhello\r\n")
        assert value == "hello"
        assert consumed == 11
        assert err is None


class TestSimpleString:
    def test_simple(self):
        value, delta, err = readSimpleString(b"+yellow\r\n")
        assert value == "yellow"
        assert delta == 9
        assert err == None

    def test_empty_string(self):
        value, delta, err = readSimpleString(b"+\r\n")
        assert value == ""
        assert delta == 3
        assert err == None

    def test_string_with_spaces(self):
        value, delta, err = readSimpleString(b"+yellow hi\r\n")
        assert value == "yellow hi"
        assert delta == 12
        assert err == None

class TestArray:
    def test_simple(self): 
        v, d, e = readArray(b"*2\r\n$1\r\nh\r\n$1\r\ne\r\n")
        assert v[0] == 'h'
        assert v[1] == 'e'
        assert d == 18
        assert e == None
    def test_simple_array(self):
        # *3\r\n$3\r\nhey\r\n$3\r\nmey\r\n$3\r\nnay\r\n
        value, consumed, err = readArray(b"*3\r\n$3\r\nhey\r\n$3\r\nmey\r\n$3\r\nnay\r\n")
        assert value == ["hey", "mey", "nay"]
        assert err is None

    def test_empty_array(self):
        # *0\r\n
        value, consumed, err = readArray(b"*0\r\n")
        assert value == []
        assert consumed == 4
        assert err is None

    def test_mixed_types(self):
        # *3\r\n+hello\r\n:42\r\n$5\r\nworld\r\n
        # Represents ['hello', 42, 'world']
        value, consumed, err = readArray(b"*3\r\n+hello\r\n:42\r\n$5\r\nworld\r\n")
        assert value == ["hello", 42, "world"]
        assert err is None

    def test_nested_array(self):
        # *2\r\n*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n*1\r\n$3\r\nbaz\r\n
        # Represents [['foo', 'bar'], ['baz']]
        value, consumed, err = readArray(b"*2\r\n*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n*1\r\n$3\r\nbaz\r\n")
        assert value == [["foo", "bar"], ["baz"]]
        assert err is None

    def test_array_of_integers(self):
        # *3\r\n:1\r\n:2\r\n:3\r\n
        # Represents [1, 2, 3]
        value, consumed, err = readArray(b"*3\r\n:1\r\n:2\r\n:3\r\n")
        assert value == [1, 2, 3]
        assert err is None

    def test_deeply_nested_array(self):
        # *1\r\n*1\r\n*1\r\n$5\r\ndeep!\r\n
        # Represents [[['deep!']]]
        value, consumed, err = readArray(b"*1\r\n*1\r\n*1\r\n$5\r\ndeep!\r\n")
        assert value == [[["deep!"]]]
        assert err is None

    def test_array_with_empty_bulk_string(self):
        # *2\r\n$0\r\n\r\n$3\r\nfoo\r\n
        # Represents ['', 'foo']
        value, consumed, err = readArray(b"*2\r\n$0\r\n\r\n$3\r\nfoo\r\n")
        assert value == ["", "foo"]
        assert err is None
