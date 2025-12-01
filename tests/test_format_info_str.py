from engine import Engine

def test_format_info_str(capsys):
    Engine("path").format_info([("depth", 1), ("seldepth", 0)])
    captured = capsys.readouterr()
    assert captured.out == "info depth 1 seldepth 0 \n"
    #or ("score", "cp 13") could also work first item
    Engine("path").format_info([("score cp", 13), ("depth", 1), ("nodes", 13), ("time", 15), ("pv", "f1b5")])
    cap1 = capsys.readouterr()
    assert cap1.out == "info score cp 13 depth 1 nodes 13 time 15 pv f1b5 \n"
    Engine("path").format_info([("depth", 2), ("seldepth", 2)])
    cap2 = capsys.readouterr()
    assert cap2.out == "info depth 2 seldepth 2 \n"
    Engine("path").format_info([("nps", 15937)])
    cap3 = capsys.readouterr()
    assert cap3.out == "info nps 15937 \n"
    Engine("path").format_info([("score cp", 14), ("depth", 2), ("nodes", 255), ("time", 15), ("pv", "f1c4 f8c5")])
    cap4 = capsys.readouterr()
    assert cap4.out == "info score cp 14 depth 2 nodes 255 time 15 pv f1c4 f8c5 \n"
    Engine("path").format_info([("depth", 2), ("seldepth", 7), ("nodes", 255)])
    cap5 = capsys.readouterr()
    assert cap5.out == "info depth 2 seldepth 7 nodes 255 \n"
    Engine("path").format_info([("depth", 3), ("seldepth", 7)])
    cap6 = capsys.readouterr()
    assert cap6.out == "info depth 3 seldepth 7 \n"
    Engine("path").format_info([("depth", 3), ("seldepth", 7)])
    cap6 = capsys.readouterr()
    assert cap6.out == "info depth 3 seldepth 7 \n"
    Engine("path").format_info([("nps", 26437)])
    cap7 = capsys.readouterr()
    assert cap7.out == "info nps 26437 \n"
    Engine("path").format_info([("score cp", 20), ("depth", 3), ("nodes", 423), ("time", 15), ("pv", "f1c4 g8f6 b1c3")])
    cap8 = capsys.readouterr()
    assert cap8.out == "info score cp 20 depth 3 nodes 423 time 15 pv f1c4 g8f6 b1c3 \n"
    Engine("path").format_info([("nps", 41562)])
    cap9 = capsys.readouterr()
    assert cap9.out == "info nps 41562 \n"
    
    

    
