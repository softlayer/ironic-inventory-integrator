================================
Inventory ReSTful API (v1)
================================

Concepts
========

1. Servers are added to the inventory manager via it's REST api.

2. Servers can be queried via the rest API to find (flavor) that match a
user's requirement.

3. When server's are queried a reservation is created to prevent subsequent
queries from attempting to provision the same hardware.

4. A user then verifies or confirms the reservation and the server is placed in
a checked-out / provisioned state.  This removes it from the pool of available
servers from subsequent queries.

5. (Planned) A user can return a check-out server to inventory.

    Note: All of the operations are intended to be independent for the bare metal
          controller and should not overlap with functionality it provides.


Servers
========

.. rest-controller:: ironic_inventory.api.controllers.v1.server:ServerController
   :webprefix: /v1/servers

.. rest-controller:: ironic_inventory.api.controllers.v1.reservation.ReservationController
   :webprefix: /v1/reservations
