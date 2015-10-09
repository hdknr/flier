========================================================================
** flier ** Installation Instructions
========================================================================

This section contains information about 
how to download and install **flier** in your system. 
It also contains brief instructions about how
to build the included documentation.

Requirements
============

Detailed information about the minimum supported Django version and 
other Python modules that may be required in order to run this software is shown below:

.. literalinclude:: ../requirements/install.txt

.. literalinclude:: ../requirements/links.txt

This information exists in the ``requirements.txt`` file 
inside the ** lots ** distribution package. 
If ``pip`` is used to install this software,
then all these dependencies will also be installed, 
if they are not already installed in your system.

Install
==============

To install **flier** from soruce code, use the provided installation script::

    python setup.py install


Or it is also possible to install this application directly from
the `source code repository`_ using ``pip``::

    pip install -e git+https://github.com/hdknr/flier.git#egg=flier

The above command will install the latest development release of **flier**.


How to build the documentation
================================

This project's documentation is located in source form under the ``docs``
directory. In order to convert the documentation to a format that is
easy to read and navigate you need the ``sphinx`` package.

You can install ``sphinx`` using ``pip``::

    pip install sphinx

Or ``easy_install``::

    easy_install sphinx

Once ``sphinx`` is installed, change to the ``docs`` directory, open a shell
and run the following command::

    make html

This will build a HTML version of the documentation. You can read the
documentation by opening the following file in any web browser::

    docs/_build/html/index.html

RabbitMQ
=============

- http://celery.readthedocs.org/en/latest/getting-started/brokers/rabbitmq.html

Debian
---------

::

    $ sudo apt-get install rabbitmq-server

::

    $ sudo service --status-all | grep rabbit
    
    [ + ]  rabbitmq-server

::

    $ sudo lsof -i:5672

    COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    beam    8220 rabbitmq   15u  IPv6  27411      0t0  TCP *:amqp (LISTEN)

Configure
------------

Virtual Host ::

    $ sudo rabbitmqctl add_vhost flier

    Creating vhost "flier" ...
    ...done.

    $ sudo rabbitmqctl list_vhosts

    Listing vhosts ...
    /
    flier
    ...done.

User::

    $ sudo rabbitmqctl add_user flier flier

    Creating user "flier" ...
    ...done.


    $ sudo rabbitmqctl list_users
    Listing users ...
    
    flier      []
    guest   [administrator]
    ...done.


Permission::

    $ sudo rabbitmqctl set_permissions -p flier flier ".*" ".*" ".*"

    Setting permissions for user "flier" in vhost "flier" ...
    ...done.

    $ sudo rabbitmqctl -p flier list_permissions

    Listing permissions in vhost "flier" ...
    flier      .*      .*      .*
    ...done.



Web
----

- https://www.rabbitmq.com/management.html

::

    $ sudo rabbitmq-plugins enable rabbitmq_management

    The following plugins have been enabled:
      mochiweb
      webmachine
      rabbitmq_web_dispatch
      amqp_client
      rabbitmq_management_agent
      rabbitmq_management
    Plugin configuration has changed. Restart RabbitMQ for changes to take effect.

::

    $ sudo service rabbitmq-server restart

::

    $ sudo lsof -i:15672

    COMMAND   PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    beam    11924 rabbitmq   18u  IPv4  35860      0t0  TCP *:15672 (LISTEN)

::

    $ zcat /usr/share/doc/rabbitmq-server/rabbitmq.config.example.gz  | sudo tee -a /etc/rabbitmq/rabbitmq.config

::

    $ sudo vim /etc/rabbitmq/rabbitmq.config

- allow guest from  other computers ( DO NOT keep the comma after the last element in a array )

::

    {loopback_users, []}         %%, 
