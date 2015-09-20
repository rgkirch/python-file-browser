" begin vundle

set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'gmarik/Vundle.vim'
Plugin 'Valloric/YouCompleteMe'
call vundle#end()
filetype plugin indent on

" end vundle

" set coloscheme
colo elflord
" a tab is 4 columns long
set tabstop=4
set shiftwidth=4
" don't convert tabs to spaces
" caries over the indentation level
set autoindent
" display line numbers
set nu
" syntax highlighting
syntax on
" i have a dark background
set background=dark
" for python files, use any python indentation guides
" au FileType *.py filetype indent plugin on
au FileType *.html colo delek

" LaTeX exponent
" visual select text and @e to convert to superscript
au FileType *.tex let @e = "da$$^[i^{}^[hp"
au BufNewFile,BufRead,BufEnter *.cpp,*.hpp set omnifunc=omni#cpp#complete#Main

autocmd CompleteDone * pclose
