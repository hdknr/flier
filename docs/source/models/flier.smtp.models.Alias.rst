virtual_alias_maps
----------------------------

main.cf 

::

    virtual_alias_maps = proxy:mysql:/etc/postfix/db/virtual_alias_maps.cf

virtual_alias_maps.cf

::

    host = localhost
    user = flier
    password = flier
    dbname = flier
    table = smtp_alias
    select_field = forward
    where_field = recipient

Definins Aliases
----------------

Alias Domain
^^^^^^^^^^^^^^^^

- Create a Domain(Alias Domaiin) model instance with local domain (like 'mailbox.local')
- Create a Domain(Receiving Domain)  model instance with actual domain (like 'service.com') with `alias_domain` created above.
  `transport` should be `error` for bounce back when Alias for `recipient` does not exists.

Aliases
^^^^^^^^^^^^

- Create any number of Alias model instanes 

    - `recipient` address domain MUST be a Receiving Domain( 'service.com')
    - `forward` address domain MUST be a Alias Domain( 'mailbox.local' )

