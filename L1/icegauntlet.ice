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

    interface Authentication{
        bool isValid(string token) throws Unauthorized;
        string getNewToken(string user,string passHash) throws Unauthorized;
        void changePassword (string user,string currentPassHash,string newPassHash) throws Unauthorized;
    };
    interface Rooms{
        string getRoom() throws RoomAlreadyExists;
        void Publish(string token, string roomData) throws Unauthorized;
        void Remove(string token, string roomName) throws RoomNotExists;
    };
};
