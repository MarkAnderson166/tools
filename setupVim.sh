#!/bin/bash

#
# SETUP VIM
#

echo "
set number
set wildmenu
set hlsearch
syntax on
set tabstop=2
set shiftwidth=2
set expandtab
set ignorecase
colo default
set nocindent
set nosmartindent
set noautoindent
set indentexpr=
highlight Comment ctermfg=blue
set laststatus=2
set statusline=%{resolve(expand('%:p'))}\ %h%m%r%y%=%-14.(%l,%c%V%)\ %P
highlight statusline guibg=blue ctermfg=blue guifg=black ctermbg=white

set nocompatible
set encoding=utf-8

let g:bufferline_echo=0

set hidden

nnoremap <silent> <C-CR> :ls<CR>:b
nnoremap <silent> <C-M> :ls<CR>:b

let netrw_keepdir=1
let g:netrw_banner=0
let g:netrw_liststyle=3
let g:netrw_list_hide='.*\.swp$'
let g:netrw_chgwin=1
let g:netrw_browse_split=3
let g:netrw_winsize=25
let g:netrw_fastbrowse=0
let g:netrw_silent=1

set history=1000
set showcmd
set showmode
set fillchars=""
set showmatch

cmap w!! w !sudo tee % > /dev/null<CR>:e!<CR><CR>

set noswapfile

highlight CursorLine cterm=NONE ctermbg=NONE ctermfg=NONE guibg=NONE guifg=NONE
set cursorline
" > ~/.vimrc
