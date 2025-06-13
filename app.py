import streamlit as st
import random

st.set_page_config(page_title="理不尽○×ゲーム", layout="centered")

# セッション状態の初期化
if 'board' not in st.session_state:
    st.session_state.board = [''] * 9
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.session_state.message = ''
    st.session_state.cpu_moves = []

# 勝利パターン定義
WIN_PATTERNS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 横
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 縦
    [0, 4, 8], [2, 4, 6]              # 斜め
]

def check_win(player):
    b = st.session_state.board
    return any(all(b[i] == player for i in pattern) for pattern in WIN_PATTERNS)

def cpu_turn():
    board = st.session_state.board
    cpu_moves = st.session_state.cpu_moves

    if st.session_state.turn == 1:
        board[4] = '○'
        cpu_moves.append(4)

    elif st.session_state.turn == 3:
        empty = [i for i in range(9) if board[i] == '']
        move = random.choice(empty)
        board[move] = '○'
        cpu_moves.append(move)

    elif st.session_state.turn == 5:
        for pattern in WIN_PATTERNS:
            filled = [i for i in pattern if i in cpu_moves]
            empty = [i for i in pattern if board[i] == '']
            if len(filled) == 2 and len(empty) == 1:
                board[empty[0]] = '○'
                cpu_moves.append(empty[0])
                break

    if check_win('○'):
        st.session_state.game_over = True
        st.session_state.message = 'CPUの勝ちです！（理不尽）'

    st.session_state.turn += 1

def player_turn(pos):
    board = st.session_state.board

    if board[pos] == '' and not st.session_state.game_over:
        board[pos] = '×'
        st.session_state.turn += 1

        if check_win('×'):
            st.session_state.game_over = True
            st.session_state.message = 'あなたの勝ちです！'
        else:
            cpu_turn()

def reset_game():
    st.session_state.board = [''] * 9
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.session_state.message = ''
    st.session_state.cpu_moves = []
    cpu_turn()

# UI表示
st.title('理不尽○×ゲーム')
st.caption('CPUは絶対に勝ちます 😈')

# ゲーム開始時にCPUの初手
if st.session_state.turn == 1 and not st.session_state.cpu_moves:
    cpu_turn()

# ゲーム盤面描画
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        index = i * 3 + j
        with cols[j]:
            if st.session_state.board[index] == '':
                if not st.session_state.game_over:
                    if st.button(" ", key=str(index), help=f"{i+1}行{j+1}列"):
                        player_turn(index)
                else:
                    st.button(" ", key=str(index), disabled=True)
            else:
                st.button(st.session_state.board[index], key=str(index), disabled=True)

# メッセージ表示
if st.session_state.message:
    st.markdown(f"### {st.session_state.message}")

# リセットボタン
if st.button('もう一度遊ぶ'):
    reset_game()
