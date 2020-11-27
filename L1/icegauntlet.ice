module IceGauntlet{
    exception Unauthorized{
        string info;
    };
    exception RoomAlreadyExists{
        string info;
    };
    exception RoomNotExists{
        string info;
    };

    interface AuthenticationI{
        bool isValid(string token) throws Unauthorized;
        string getNewToken(string user,string passHash) throws Unauthorized;
        void changePassword (string user,string currentPassHash,string newPassHash) throws Unauthorized;
    };
    interface Server{
        string getRoom() throws RoomAlreadyExists;
        void Publish(string token, string roomData) throws Unauthorized;
        void Remove(string token, string roomName) throws RoomNotExists;
    };
};
