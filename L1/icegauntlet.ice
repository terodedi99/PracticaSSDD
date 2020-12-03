module IceGauntlet{
    exception Unauthorized{};
    exception RoomAlreadyExists{};
    exception RoomNotExists{};
    exception WrongRoomFormat{};

    interface Authentication{
        bool isValid(string token) throws Unauthorized;
        string getNewToken(string user,string passHash) throws Unauthorized;
        void changePassword (string user,string currentPassHash,string newPassHash) throws Unauthorized;
    };
    interface RoomManager{
        void Publish(string token, string roomData) throws Unauthorized, RoomAlreadyExists, WrongRoomFormat;
        void Remove(string token, string roomName) throws Unauthorized, RoomNotExists;
    };
    interface Dungeon {
        string getRoom() throws RoomNotExists;
    };
};
