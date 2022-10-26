/*
 Tutorial/Example/seven.cc
 */

#include <fstream>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/stats-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("task_2");

// ===========================================================================
//
//         node 0                 node 1
//   +----------------+    +----------------+
//   |    ns-3 TCP    |    |    ns-3 TCP    |
//   +----------------+    +----------------+
//   |    10.1.1.1    |    |    10.1.1.2    |
//   +----------------+    +----------------+
//   | point-to-point |    | point-to-point |
//   +----------------+    +----------------+
//           |                     |
//           +---------------------+
//
//
//
// ===========================================================================
//

int dropPacketCount = 0;
uint32_t maxCwd = 0;
class MyApp : public Application
{
public:
    MyApp();
    virtual ~MyApp();
    static TypeId GetTypeId(void);
    void Setup(Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);

private:
    virtual void StartApplication(void);
    virtual void StopApplication(void);

    void ScheduleTx(void);
    void SendPacket(void);

    Ptr<Socket> m_socket;
    Address m_peer;
    uint32_t m_packetSize;
    uint32_t m_nPackets;
    DataRate m_dataRate;
    EventId m_sendEvent;
    bool m_running;
    uint32_t m_packetsSent;
};

MyApp::MyApp()
    : m_socket(0),
      m_peer(),
      m_packetSize(0),
      m_nPackets(0),
      m_dataRate(0),
      m_sendEvent(),
      m_running(false),
      m_packetsSent(0)
{
}

MyApp::~MyApp()
{
    m_socket = 0;
}

/* static */
TypeId MyApp::GetTypeId(void)
{
    static TypeId tid = TypeId("MyApp")
                            .SetParent<Application>()
                            .SetGroupName("ASS3")
                            .AddConstructor<MyApp>();
    return tid;
}

void MyApp::Setup(Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate)
{
    m_socket = socket;
    m_peer = address;
    m_packetSize = packetSize;
    m_nPackets = nPackets;
    m_dataRate = dataRate;
}

void MyApp::StartApplication(void)
{
    m_running = true;
    m_packetsSent = 0;
    if (InetSocketAddress::IsMatchingType(m_peer))
    {
        m_socket->Bind();
    }
    else
    {
        m_socket->Bind6();
    }
    m_socket->Connect(m_peer);
    SendPacket();
}

void MyApp::StopApplication(void)
{
    m_running = false;

    if (m_sendEvent.IsRunning())
    {
        Simulator::Cancel(m_sendEvent);
    }

    if (m_socket)
    {
        m_socket->Close();
    }
}

void MyApp::SendPacket(void)
{
    Ptr<Packet> packet = Create<Packet>(m_packetSize);
    m_socket->Send(packet);

    if (++m_packetsSent < m_nPackets)
    {
        ScheduleTx();
    }
}

void MyApp::ScheduleTx(void)
{
    if (m_running)
    {
        Time tNext(Seconds(m_packetSize * 8 / static_cast<double>(m_dataRate.GetBitRate())));
        m_sendEvent = Simulator::Schedule(tNext, &MyApp::SendPacket, this);
    }
}

static void
CwndChange(Ptr<OutputStreamWrapper> stream, uint32_t oldCwnd, uint32_t newCwnd)
{
    NS_LOG_UNCOND(Simulator::Now().GetSeconds() << "\t" << newCwnd);
    // *stream->GetStream() << Simulator::Now().GetSeconds() << "\t" << oldCwnd << "\t" << newCwnd << std::endl;
    *stream->GetStream() << Simulator::Now().GetSeconds() << "\t" << newCwnd << std::endl;
    maxCwd = std::max(maxCwd,newCwnd);
}

// static void
// RxDrop(Ptr<PcapFileWrapper> file, Ptr<const Packet> p)
// {
//     NS_LOG_UNCOND("RxDrop at " << Simulator::Now().GetSeconds());
//     file->Write(Simulator::Now(), p);
//     dropPacketCount += 1;
// }

int main(int argc, char *argv[])
{


    Config::SetDefault ("ns3::TcpL4Protocol::SocketType",  TypeIdValue (TypeId::LookupByName("ns3::TcpVegas")));

    CommandLine cmd;
    cmd.Parse(argc, argv);

    NodeContainer nodes;
    nodes.Create(5);

    NodeContainer connections[4];
    connections[0] = NodeContainer(nodes.Get(0),nodes.Get(1));
    connections[1] = NodeContainer(nodes.Get(1),nodes.Get(2));
    connections[2] = NodeContainer(nodes.Get(2),nodes.Get(3));
    connections[3] = NodeContainer(nodes.Get(2),nodes.Get(4));


    PointToPointHelper pointToPoint;
    pointToPoint.SetDeviceAttribute("DataRate", StringValue("500Kbps"));
    pointToPoint.SetChannelAttribute("Delay", StringValue("3ms"));

    InternetStackHelper stack;
    stack.Install(nodes);


    std::vector<NetDeviceContainer> deviceAdjacencyList(4);
    for(uint32_t i=0; i<deviceAdjacencyList.size (); ++i)
    {
      deviceAdjacencyList[i] = pointToPoint.Install (connections[i]);
    }     

    Ipv4AddressHelper ipv4;
    std::vector<Ipv4InterfaceContainer> interfaceAdjacencyList (4);
    for(uint32_t i=0; i<interfaceAdjacencyList.size (); ++i)
    {
      std::ostringstream subnet;
      subnet<<"10.1."<<i+1<<".0";
      ipv4.SetBase (subnet.str ().c_str (), "255.255.255.0");
      interfaceAdjacencyList[i] = ipv4.Assign (deviceAdjacencyList[i]);
    }

    Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

    Ptr<RateErrorModel> em = CreateObject<RateErrorModel>();
    em->SetAttribute("ErrorRate", DoubleValue(0.00001));
    deviceAdjacencyList[2].Get(1)->SetAttribute("ReceiveErrorModel", PointerValue(em));


    uint16_t sinkPort = 8080;

    Address sinkAddress;
    Address anyAddress;

    sinkAddress = InetSocketAddress(interfaceAdjacencyList[2].GetAddress(1), sinkPort);
    
    //Might be trouble
    anyAddress = InetSocketAddress(Ipv4Address::GetAny(), sinkPort);



    std::string probeType;
    std::string tracePath;

    probeType = "ns3::Ipv4PacketProbe";
    tracePath = "/NodeList/*/$ns3::Ipv4L3Protocol/Tx";
    

    PacketSinkHelper tcp_sink_helper("ns3::TcpSocketFactory", anyAddress);
    ApplicationContainer sinkApps = tcp_sink_helper.Install(nodes.Get(3));
    sinkApps.Start(Seconds(0.0));
    sinkApps.Stop(Seconds(100.0));



    Ptr<Socket> ns3TcpSocket = Socket::CreateSocket(nodes.Get(0), TcpSocketFactory::GetTypeId());

    Ptr<MyApp> app = CreateObject<MyApp>();
    app->Setup(ns3TcpSocket, sinkAddress, 1040, 100000, DataRate("250Kbps"));
    nodes.Get(0)->AddApplication(app);
    app->SetStartTime(Seconds(1.0));
    app->SetStopTime(Seconds(100.0));




    uint16_t udp_port = 6969;

    OnOffHelper onoff ("ns3::UdpSocketFactory", 
                     Address (InetSocketAddress (interfaceAdjacencyList[3].GetAddress (1), udp_port)));

    onoff.SetConstantRate (DataRate ("250Kbps"));
    ApplicationContainer udpapp = onoff.Install (nodes.Get (1));

    udpapp.Start (Seconds (20.0));
    udpapp.Stop (Seconds (30.0));

    onoff.SetConstantRate (DataRate ("500Kbps"));

    udpapp = onoff.Install (nodes.Get (1));
    udpapp.Start (Seconds (30.0));
    udpapp.Stop (Seconds (100.0));

    PacketSinkHelper usink ("ns3::UdpSocketFactory",
                         Address (InetSocketAddress (Ipv4Address::GetAny (), udp_port)));
    udpapp = usink.Install (nodes.Get (4));
    udpapp.Start (Seconds (20.0));
    udpapp.Stop (Seconds (100.0));



    // UdpServerHelper server (udp_port);
    // ApplicationContainer udpapp = server.Install (nodes.Get (1));
    // udpapp.Start (Seconds (0.0));
    // udpapp.Stop (Seconds (100.0));


    // Address udp_serverAddress;
    // udp_serverAddress = Address (interfaceAdjacencyList[3].GetAddress (1));

    // uint32_t MaxPacketSize = 1040;
    // // Time interPacketInterval = Seconds (0.05);
    // uint32_t maxPacketCount = 100000;

    // UdpClientHelper client (udp_serverAddress, udp_port);

    // client.SetAttribute ("MaxPackets", UintegerValue (maxPacketCount));
    // // client.SetAttribute ("Interval", TimeValue (interPacketInterval));
    // client.SetAttribute ("PacketSize", UintegerValue (MaxPacketSize));
    // udpapp = client.Install (nodes.Get(4));
    // udpapp.Start (Seconds (1.0));
    // udpapp.Stop (Seconds (1000.0));



    AsciiTraceHelper asciiTraceHelper;
    Ptr<OutputStreamWrapper> stream = asciiTraceHelper.CreateFileStream("task_3.dat");
    ns3TcpSocket->TraceConnectWithoutContext("CongestionWindow", MakeBoundCallback(&CwndChange, stream));

    // PcapHelper pcapHelper;
    // Ptr<PcapFileWrapper> file = pcapHelper.CreateFile("task_2_" + cDataRate + aDataRate + ".pcap", std::ios::out, PcapHelper::DLT_PPP);
    // devices.Get(1)->TraceConnectWithoutContext("PhyRxDrop", MakeBoundCallback(&RxDrop, file));

    pointToPoint.EnablePcapAll ("task_3_pcap");

    // Use FileHelper to write out the packet byte count over time
    FileHelper fileHelper;

    // Configure the file to be written, and the formatting of output data.
    fileHelper.ConfigureFile("task_3_packet-byte-count",
                             FileAggregator::FORMATTED);

    // Set the labels for this formatted output file.
    fileHelper.Set2dFormat("Time (Seconds) = %.3e\tPacket Byte Count = %.0f");

    // Specify the probe type, trace source path (in configuration namespace), and
    // probe output trace source ("OutputBytes") to write.
    fileHelper.WriteProbe(probeType,
                          tracePath,
                          "OutputBytes");

    Simulator::Stop(Seconds(100));
    Simulator::Run();
    Simulator::Destroy();

    // std::cout << "Max CWD " << proto_ << ": " << maxCwd << std::endl;
    // std::cout << "No of packet drops for " << proto_ << ": " << dropPacketCount << std::endl;

    return 0;
}
