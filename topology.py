from mininet.topo import Topo

class TriangleTopo(Topo):
    """Simple triangle topology with 3 switches and 2 hosts.
       Creates a triangle with two paths between h1 and h2:

       h1 --- s1 --- s2 --- h2
              |      |
              +---s3---+

       This creates two paths: h1->s1->s2->h2 and h1->s1->s3->h2
    """

    def build(self):
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add links
        # Host connections
        self.addLink(h1, s1)
        self.addLink(h2, s2)

        # Switch connections - creating the triangle
        self.addLink(s1, s2)  # Direct path
        self.addLink(s1, s3)  # Alternative path part 1
        self.addLink(s3, s2)  # Alternative path part 2

# Register the topology
topos = {'triangle': (lambda: TriangleTopo())}