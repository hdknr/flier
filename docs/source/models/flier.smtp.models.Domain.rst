transport_maps
---------------


transport_maps.cf  sample configuration

::

    host = localhost
    user = flier
    password = flier
    dbname = flier
    table = smtp_domain
    select_field = transport
    where_field = domain

main.cf

::

    transport_maps = proxy:mysql:/etc/postfix/db/transport_maps.cf



relay_domain
-------------------

relay_domains.cf Sample configuration

::

    hosts = localhost
    dbname = flier
    user = flier
    password = flier
    table = smtp_domain
    select_field = domain
    where_field = domain

main.cf

::

    relay_domains = proxy:mysql:/etc/postfix/db/relay_domains.cf



transport
----------

Service Name
^^^^^^^^^^^^^^^

- http://www.postfix.org/master.5.html

Command

- http://www.postfix.org/pipe.8.html


STMP Address
^^^^^^^^^^^^^

::

    smtp:[192.168.56.51]


default transport
---------------------

Mainly for testing.

main.cf

::

    default_transport=jail



master
----------

Sample pipe transport

::

    jail unix  -       n       n       -       -       pipe
      flags=FDRq user=vagrant argv=/home/vagrant/inbound.sh jail $sender $recipient $original_recipient

    inbound unix  -       n       n       -       -       pipe
      flags=FDRq user=vagrant argv=/home/vagrant/inbound.sh inbound $sender $recipient $original_recipient

    mailbox unix  -       n       n       -       -       pipe
      flags=FDRq user=vagrant argv=/home/vagrant/inbound.sh mailbox $sender $recipient $original_recipient

inbound.sh like this:

.. code-block:: bash

    #!/bin/sh
    PY=/home/vagrant/.anyenv/envs/pyenv/versions/dev/bin/python
    MN=/home/vagrant/.anyenv/envs/pyenv/versions/dev/src/flier/sample/manage.py
    
    $PY $MN fliersmtp bounce $@
