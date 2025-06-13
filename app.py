import streamlit as st
import random

# 初期化
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(5)] for _ in range(5)]
    st.session_state.turn = 0
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.cpu_moves = []

# 勝利判定（5x5対応）
def check_win(mark):
    board = st.session_state.board
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

# CPUの行動
def cpu_move():
    board = st.session_state.board
    cpu_turn = st.session_state.turn

    if cpu_turn == 0:
        board[2][2] = "〇"  # 中央
        st.session_state.cpu_moves.append((2, 2))
    elif cpu_turn == 2:
        # ランダムに可視3x3範囲から未使用マスを探す
        empty = [(r, c) for r in range(1, 4) for c in range(1, 4) if board[r][c] == ""]
        if empty:
            r, c = random.choice(empty)
            board[r][c] = "〇"
            st.session_state.cpu_moves.append((r, c))
    elif cpu_turn == 4:
        # 最後に「不可視」マス(0行や4行/列)を使って直線にする
        (r1, c1), (r2, c2) = st.session_state.cpu_moves
        dr = r2 - r1
        dc = c2 - c1
        r3 = r2 + dr
        c3 = c2 + dc
        # 画面外(0か4)を狙うように調整
        r3 = max(0, min(4, r3))
        c3 = max(0, min(4, c3))
        board[r3][c3] = "〇"
        st.session_state.cpu_moves.append((r3, c3))
        if check_win("〇"):
            st.session_state.message = "CPUの勝ちです！"
            st.session_state.game_over = True

# プレイヤーの操作
def player_move(r, c):
    if st.session_state.board[r][c] != "" or st.session_state.game_over:
        return
    st.session_state.board[r][c] = "×"
    if check_win("×"):
        st.session_state.message = "あなたの勝ちです！"
        st.session_state.game_over = True

# 描画
st.title("○×ゲーム（CPU理不尽勝利モード）")

if not st.session_state.game_over and st.session_state.turn % 2 == 0:
    cpu_move()

for r in range(1, 4):
    cols = st.columns(3)
    for c in range(1, 4):
        cell = st.session_state.board[r][c]
        if cell == "":
            if not st.session_state.game_over:
                if cols[c-1].button(" ", key=f"{r}-{c}"):
                    player_move(r, c)
                    st.session_state.turn += 1
        else:
            cols[c-1].button(cell, key=f"{r}-{c}", disabled=True)

# CPUのターンが後に控えている場合、自動で回す
if not st.session_state.game_over and st.session_state.turn % 2 == 1:
    st.session_state.turn += 1
    cpu_move()

st.write("----")
st.write(st.session_state.message)

# リセット
if st.button("リセット"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
