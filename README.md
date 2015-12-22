bck
===

[bck](https://github.com/truncator/bck/) is a simple command line interface remote backup script using rsync and ssh.

Installation
----------

```
chmod +x install && ./install
```

`bck` is installed to `~/bin` by default. This can be changed in `install`.

Usage
-----

```
$ usage: bck list
         bck push <source>
         bck pull [<source>]
```

Examples
-----

``` bash
$ bck list
total 0
```

``` bash
$ bck push bck.py bckrc
$ bck list
total 8.0K
-rwxr-xr-x 1 trn 3.5K Jul 10 23:55 bck.py
-rw-r--r-- 1 trn  188 Jul 10 23:03 bckrc
```

``` bash
$ cd ~/some/dir
$ bck pull bckrc
```

Dependencies
------------

* OpenSSH
* Python 3+
* rsync
