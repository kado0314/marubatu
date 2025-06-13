import streamlit as st
import time

# 初期化
if "board5" not in st.session_state:
    st.session_state.board5 = [["" for _ in range(5)] for _ in range(5)]  # 5x5
    st.session_state.turn = 0
    st.session_state.message = ""
    st.session_state.game_over = False
    st.session_state.show_full_board = False
    st.session_state.last_player_move = None
    

# 勝利判定（3つそろい）
def check_win(mark, board):
    for r in range(5):
        for c in range(3):
            if all(board[r][c+i] == mark for i in range(3)):
                return True
    for c in range(5):
        for r in range(3):
            if all(board[r+i][c] == mark for i in range(3)):
                return True
    for r in range(3):
        for c in range(3):
            if all(board[r+i][c+i] == mark for i in range(3)):
                return True
            if all(board[r+2-i][c+i] == mark for i in range(3)):
                return True
    return False

# CPUの固定手順に従う
def cpu_move(turn):
    board = st.session_state.board5
    last_player_move = st.session_state.last_player_move
    daruset=None
    if turn == 0:
        board[2][2] = "〇"  # 一手目
    elif turn == 2:
        r, c = last_player_move
        if r==1 and c==3:
            board[2][3] = "〇"
            daruset=True
        else:
            board[1][3] = "〇"  # 三手目 (見える3x3に追加)
            daruset=False
    elif turn == 4:
        # 5ターン目：5x5に切り替え、直線で勝ち
        st.session_state.show_full_board = True
        if daruset:
            board[2][4] = "〇" 
        else:
            board[0][4] = "〇"  
        st.session_state.message = "CPUの勝ちです！（理不尽）"
        st.session_state.game_over = True

# プレイヤーの操作
def player_move(r, c):
    board = st.session_state.board5
    if board[r][c] != "" or st.session_state.game_over:
        return
    board[r][c] = "×"
    st.session_state.last_player_move = (r, c)
    if check_win("×", board):
        st.session_state.message = "あなたの勝ちです！"
        st.session_state.game_over = True
    st.session_state.turn += 1

# 描画スタート
st.title("○×ゲーム（CPU勝ち固定モード）")

turn = st.session_state.turn
board = st.session_state.board5

# 表示ターン
if not st.session_state.game_over:
    if turn % 2 == 0:
        st.subheader("🧠 CPUの番です...")
        with st.spinner("CPUが考えています..."):
            time.sleep(1.5)
            cpu_move(turn)
            st.session_state.turn += 1
        st.rerun()
    else:
        st.subheader("🧍 あなたの番です")

# 描画：3x3 か 5x5
rows = range(1, 4)
cols = range(1, 4)
if st.session_state.show_full_board:
    rows = range(5)
    cols = range(5)
    st.subheader("🌐 最終盤面：5x5")

# ボード描画
for r in rows:
    cols_obj = st.columns(len(cols))
    for i, c in enumerate(cols):
        val = board[r][c]
        if val == "":
            if not st.session_state.game_over and turn % 2 == 1:
                if cols_obj[i].button(" ", key=f"{r}-{c}"):
                    player_move(r, c)
        else:
            cols_obj[i].button(val, key=f"{r}-{c}", disabled=True)

st.write("---")
st.write(st.session_state.message)

if st.button("🔄 リセット"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()
