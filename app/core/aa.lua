local export_array = {}

local ffi = require('ffi')
local setupapi = ffi.load('SetupAPI.dll')
local advapi32 = ffi.load('Advapi32.dll')

local WM_INPUTLANGCHANGEREQUEST = 0x0050
local INPUTLANGCHANGE_SYSCHARSET = 0x0001
local DIGCF_ALLCLASSES = 4
local DIGCF_PRESENT = 2
local SPDRP_HARDWAREID = 1
local DICS_FLAG_GLOBAL = 1
local DIREG_DEV = 1
local KEY_READ = 131097
local BUFF_LEN = 20
local ERROR_SUCCESS = 0
local REG_SZ = 1
local TRUE = 1
local FALSE = 0
local GENERIC_READ =  0x80000000
local GENERIC_WRITE = 0x40000000
local NULL = 0
local OPEN_EXISTING = 3
local FILE_FLAG_OVERLAPPED = 0x40000000
local DTR_CONTROL_DISABLE = 0x00
local RTS_CONTROL_DISABLE = 0x00
local INVALID_HANDLE_VALUE = -1
local PURGE_RXCLEAR = 0x0008
local PURGE_TXCLEAR = 0x0004
local EV_RXCHAR = 0x0001
local INFINITE = 0xFFFFFFFF
local WAIT_OBJECT_0 = 0
local BUFSIZE = 64



ffi.cdef[[
struct HWND__ { int unused; }; typedef struct HWND__ *HWND;
struct HKEY__ { int unused; }; typedef struct HKEY__ *HKEY;
struct HKL__ { int unused; }; typedef struct HKL__ *HKL;

typedef unsigned short WORD;
typedef unsigned int    UINT;
typedef char            CHAR;
typedef short           SHORT;
typedef long        LONG_PTR;
typedef unsigned int UINT_PTR;
typedef LONG_PTR LRESULT;
typedef UINT_PTR WPARAM;
typedef LONG_PTR LPARAM;
typedef HKEY *PHKEY;
typedef unsigned long ULONG;
typedef unsigned long   DWORD;
typedef DWORD         *LPDWORD;
typedef long   LONG;
typedef DWORD *PDWORD;
typedef unsigned char BYTE;
typedef BYTE *PBYTE, *LPBYTE;
typedef wchar_t         WCHAR;
typedef const char      *LPCSTR, *PCSTR;
typedef unsigned long ULONG_PTR, *PULONG_PTR;
typedef void *PVOID;
typedef PVOID HDEVINFO;
typedef ULONG DEVPROPTYPE;
typedef LONG LSTATUS;
typedef DWORD ACCESS_MASK;
typedef ACCESS_MASK REGSAM;

typedef struct _GUID {unsigned long Data1; unsigned short Data2; unsigned short Data3; unsigned char Data4[8];} GUID;
typedef struct _SP_DEVINFO_DATA {DWORD cbSize; GUID ClassGuid; DWORD DevInst; ULONG_PTR Reserved;} SP_DEVINFO_DATA, *PSP_DEVINFO_DATA;

HDEVINFO SetupDiGetClassDevsA(const GUID *ClassGuid, PCSTR Enumerator, HWND hwndParent, DWORD Flags);
bool SetupDiDestroyDeviceInfoList(HDEVINFO DeviceInfoSet);
bool SetupDiEnumDeviceInfo(HDEVINFO DeviceInfoSet, DWORD MemberIndex, PSP_DEVINFO_DATA DeviceInfoData);
bool SetupDiGetDeviceRegistryPropertyA(HDEVINFO DeviceInfoSet, PSP_DEVINFO_DATA DeviceInfoData, DWORD Property,
    PDWORD PropertyRegDataType, PBYTE PropertyBuffer, DWORD PropertyBufferSize, PDWORD RequiredSize);
HKEY SetupDiOpenDevRegKey(HDEVINFO DeviceInfoSet, PSP_DEVINFO_DATA DeviceInfoData,
  DWORD Scope, DWORD HwProfile, DWORD KeyType, REGSAM samDesired);
LSTATUS RegCloseKey(HKEY hKey);
LSTATUS RegQueryValueExA(HKEY hKey, LPCSTR lpValueName, LPDWORD lpReserved, LPDWORD lpType,LPBYTE lpData, LPDWORD lpcbData);
HKL LoadKeyboardLayoutA(LPCSTR pwszKLID, UINT Flags);
HWND GetForegroundWindow();
SHORT VkKeyScanExA(CHAR ch, HKL dwhkl);
LRESULT SendMessageA(HWND hWnd, UINT Msg, WPARAM wParam, LPARAM lParam);
HKL GetKeyboardLayout(DWORD idThread);
DWORD GetWindowThreadProcessId(HWND hWnd, LPDWORD lpdwProcessId);

typedef struct _COMSTAT {DWORD fCtsHold : 1; DWORD fDsrHold : 1; DWORD fRlsdHold : 1; DWORD fXoffHold : 1; DWORD fXoffSent : 1;
  DWORD fEof : 1; DWORD fTxim : 1; DWORD fReserved : 25; DWORD cbInQue; DWORD cbOutQue;} COMSTAT, *LPCOMSTAT;
typedef struct _DCB {DWORD DCBlength; DWORD BaudRate; DWORD fBinary : 1; DWORD fParity : 1; DWORD fOutxCtsFlow : 1; DWORD fOutxDsrFlow : 1;
  DWORD fDtrControl : 2; DWORD fDsrSensitivity : 1; DWORD fTXContinueOnXoff : 1; DWORD fOutX : 1; DWORD fInX : 1; DWORD fErrorChar : 1;
  DWORD fNull : 1; DWORD fRtsControl : 2; DWORD fAbortOnError : 1; DWORD fDummy2 : 17; WORD  wReserved; WORD  XonLim; WORD  XoffLim; BYTE  ByteSize;
  BYTE  Parity; BYTE  StopBits; char  XonChar; char  XoffChar; char  ErrorChar; char  EofChar;  char  EvtChar; WORD  wReserved1;} DCB, *LPDCB;
typedef struct _COMMTIMEOUTS {DWORD ReadIntervalTimeout; DWORD ReadTotalTimeoutMultiplier; DWORD ReadTotalTimeoutConstant;
  DWORD WriteTotalTimeoutMultiplier; DWORD WriteTotalTimeoutConstant;} COMMTIMEOUTS, *LPCOMMTIMEOUTS;
typedef struct _OVERLAPPED {unsigned long Internal; unsigned long InternalHigh;
  union { struct { DWORD Offset; DWORD OffsetHigh;} DUMMYSTRUCTNAME; void* Pointer;} DUMMYUNIONNAME;
  int  hEvent;} OVERLAPPED, *LPOVERLAPPED;
int CreateFileA(const char* lpFileName, DWORD dwDesiredAccess, DWORD dwShareMode,
  int lpSecurityAttributes, DWORD dwCreationDisposition, DWORD dwFlagsAndAttributes, int hTemplateFile);
bool CloseHandle(int hObject);
bool GetCommState(int hFile, LPDCB lpDCB);
bool SetCommState(int hFile, LPDCB lpDCB);
bool SetCommTimeouts(int hFile, LPCOMMTIMEOUTS lpCommTimeouts);
bool SetupComm(int hFile, DWORD dwInQueue, DWORD dwOutQueue);
bool PurgeComm(int hFile, DWORD dwFlags);
int CreateEventA(int lpEventAttributes, bool bManualReset, bool bInitialState, const char* lpName);
bool SetCommMask(int hFile, DWORD dwEvtMask);
bool WaitCommEvent(int hFile, unsigned long* lpEvtMask, LPOVERLAPPED lpOverlapped);
DWORD WaitForSingleObject(int hHandle, DWORD dwMilliseconds);
bool GetOverlappedResult(int hFile, LPOVERLAPPED lpOverlapped, unsigned long* lpNumberOfBytesTransferred, int bWait);
bool ClearCommError(int hFile, unsigned long* lpErrors, LPCOMSTAT lpStat);
bool ReadFile(int hFile, unsigned char* lpBuffer, DWORD nNumberOfBytesToRead, unsigned long* lpNumberOfBytesRead, LPOVERLAPPED lpOverlapped);
bool WriteFile(int hFile, unsigned char* lpBuffer, DWORD nNumberOfBytesToWrite, unsigned long* lpNumberOfBytesWritten, LPOVERLAPPED lpOverlapped);
]]

local hkl419 = ffi.C.LoadKeyboardLayoutA("00000419", 0)
local hkl409 = ffi.C.LoadKeyboardLayoutA("00000409", 0)

export_array.com = 5          -- номер порта
export_array.delay_key = 20   -- пауза между нажатиями клавиш. Только чтение, изменение через set_delay_key.
export_array.delay_mouse = 20 -- пауза между нажатием и отпусканием кнопок мыши. Только чтение, изменение через set_delay_mouse.
export_array.delay_mousemove = 0  -- пауза при перемещении курсора
export_array.offset_mousemove = 3 -- смещение курсора по x и y при перемещении мыши
export_array.random_delay_key = 0  -- рандом между нажатием и отпусканием клавиши клавиатуры
export_array.random_delay_mouse = 0  -- рандом между нажатием и отпусканием клавиши мыши

export_array.mouse_left_button = 1
export_array.mouse_right_button = 2
export_array.mouse_middle_button = 4

export_array.left_ctrl = 0x80
export_array.left_shift = 0x81
export_array.left_alt = 0x82
export_array.left_gui = 0x83
export_array.right_ctrl = 0x84
export_array.right_shift = 0x85
export_array.right_alt = 0x86
export_array.right_gui = 0x87
export_array.up_arrow = 0xDA
export_array.down_arrow = 0xD9
export_array.left_arrow = 0xD8
export_array.right_arrow = 0xD7
export_array.backspace = 0xB2
export_array.tab = 0xB3
export_array.enter = 0xB0
export_array.esc = 0xB1
export_array.insert = 0xD1
export_array.delete = 0xD4
export_array.page_up = 0xD3
export_array.page_down = 0xD6
export_array.home = 0xD2
export_array["end"] = 0xD5
export_array.caps_lock = 0xC1
export_array.f1 = 0xC2
export_array.f2 = 0xC3
export_array.f3 = 0xC4
export_array.f4 = 0xC5
export_array.f5 = 0xC6
export_array.f6 = 0xC7
export_array.f7 = 0xC8
export_array.f8 = 0xC9
export_array.f9 = 0xCA
export_array.f10 = 0xCB
export_array.f11 = 0xCC
export_array.f12 = 0xCD
export_array.F1 = 0xC2
export_array.F2 = 0xC3
export_array.F3 = 0xC4
export_array.F4 = 0xC5
export_array.F5 = 0xC6
export_array.F6 = 0xC7
export_array.F7 = 0xC8
export_array.F8 = 0xC9
export_array.F9 = 0xCA
export_array.F10 = 0xCB
export_array.F11 = 0xCC
export_array.F12 = 0xCD

local command = function (text)
    local dcb = ffi.new('DCB')
    local timeouts = ffi.new('COMMTIMEOUTS', {0, 0, 0, 0, 0})
    local bufrd = ffi.new('unsigned char[?]', BUFSIZE, 0)
    local bufwr = ffi.new('unsigned char[?]', BUFSIZE, 0)
    local overlapped = ffi.new('OVERLAPPED', 0)
    local overlappedwr = ffi.new('OVERLAPPED', 0)
    local comstat = ffi.new('COMSTAT', 0)
    local temp = ffi.new('unsigned long[1]', 0)
    local mask = ffi.new('unsigned long[1]', 0)

    dcb.DCBlength = ffi.sizeof(dcb)
    dcb.BaudRate = 9600;
    dcb.fBinary = TRUE;
    dcb.fOutxCtsFlow = FALSE;
    dcb.fOutxDsrFlow = FALSE;
    dcb.fDtrControl = DTR_CONTROL_DISABLE;
    dcb.fDsrSensitivity = FALSE;
    dcb.fNull = FALSE;
    dcb.fRtsControl = RTS_CONTROL_DISABLE;
    dcb.fAbortOnError = FALSE;
    dcb.ByteSize = 8;
    dcb.Parity = 0;
    dcb.StopBits = 0;


    local COMport
    repeat
        COMport = ffi.C.CreateFileA('COM' .. tostring(export_array.com), GENERIC_READ + GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_FLAG_OVERLAPPED, NULL)
        if COMport == INVALID_HANDLE_VALUE then wait (1) end
    until COMport ~= INVALID_HANDLE_VALUE

    if ffi.C.GetCommState(COMport, dcb) == 0 then
        log('Не удалось считать DCB')
        ffi.C.CloseHandle (COMport)
        end_script()
    end

    if ffi.C.SetCommState(COMport, dcb) == 0 then
        log('Не удалось установить DCB')
        ffi.C.CloseHandle (COMport)
        end_script()
    end

    if ffi.C.SetCommTimeouts(COMport, timeouts) == 0 then
        log('"Не удалось установить тайм-ауты')
        ffi.C.CloseHandle (COMport)
        end_script()
    end

    ffi.C.SetupComm(COMport,BUFSIZE,BUFSIZE)
    ffi.C.PurgeComm(COMport, PURGE_RXCLEAR)

    ffi.copy(bufwr, text)    -- команда

    overlappedwr.hEvent = ffi.C.CreateEventA(NULL, true, true, nil)
    ffi.C.WriteFile(COMport, bufwr, ffi.string(bufwr):len(), temp, overlappedwr)
    signal = ffi.C.WaitForSingleObject(overlappedwr.hEvent, INFINITE)

    if signal == WAIT_OBJECT_0 and ffi.C.GetOverlappedResult(COMport, overlappedwr, temp, true) then
        ffi.C.CloseHandle(overlappedwr.hEvent)
    end

    overlapped.hEvent = ffi.C.CreateEventA(NULL, true, true, nil)
    ffi.C.SetCommMask(COMport, EV_RXCHAR)
    ffi.C.WaitCommEvent(COMport, mask, overlapped)

    local signal = ffi.C.WaitForSingleObject(overlapped.hEvent, INFINITE)
    if signal == WAIT_OBJECT_0 then
        if ffi.C.GetOverlappedResult(COMport, overlapped, temp, true) then
            ffi.C.ClearCommError(COMport, temp, comstat)
            if comstat.cbInQue > 0 then
                ffi.C.ReadFile(COMport, bufrd, comstat.cbInQue, temp, overlapped)
                ffi.C.CloseHandle(overlapped.hEvent)
            end

        end
    end
    ffi.C.CloseHandle (COMport)
end


export_array.set_delay_key = function (ms)
    if type(tonumber(ms)) ~= 'number' then return end
    command ('00' .. tostring(ms))
    export_array.delay_key = ms
end

export_array.set_delay_mouse = function (ms)
    if type(tonumber(ms)) ~= 'number' then return end
    command ('01' .. tostring(ms))
    export_array.delay_mouse = ms
end

export_array.set_delay_mousemove = function (ms)
    if type(tonumber(ms)) ~= 'number' then return end
    if ms < 0 then ms = 0 end
    command ('02' .. tostring(ms))
    export_array.delay_mousemove = ms
end

export_array.set_offset_mousemove = function (step)
    if type(tonumber(step)) ~= 'number' then return end
    if step < 1 or step > 127 then step = 127 end
    command ('03' .. tostring(step))
    export_array.offset_mousemove = step
end

export_array.set_random_delay_key = function (rand)
    if type(tonumber(rand)) ~= 'number' then return end
    command ('04' .. tostring(rand))
    export_array.random_delay_key = rand
end

export_array.set_random_delay_mouse = function (rand)
    if type(tonumber(rand)) ~= 'number' then return end
    command ('05' .. tostring(rand))
    export_array.random_delay_mouse = rand
end




export_array.key = function (code)
     if type(code) == 'number' then command ('1' .. tostring(tonumber(code)))
     else command ('1' .. tostring(code:byte()))
     end
end


export_array.text = function(text)
    if type(text) ~= 'string' then return end
    local ProcessId = ffi.new('LPDWORD')
    local ThreadID = ffi.C.GetWindowThreadProcessId(ffi.C.GetForegroundWindow(), ProcessId)
    local Layout = ffi.C.GetKeyboardLayout(ThreadID)   -- запомнить раскладку до вызова функции
    local CurrentLayout = Layout
    for symbol in text:gmatch(".") do
        local vk
        if symbol:byte() > 191 or symbol:byte() == 184 or symbol:byte() == 168 then  -- если русский символ
            if CurrentLayout ~= hkl419 then   -- если текущая раскладка не англ.
                ffi.C.SendMessageA(ffi.C.GetForegroundWindow(), WM_INPUTLANGCHANGEREQUEST, INPUTLANGCHANGE_SYSCHARSET, ffi.cast('LPARAM', hkl419))
                CurrentLayout = hkl419
            end
	    vk = ffi.C.VkKeyScanExA(symbol:byte(), hkl419)
		else
			if CurrentLayout ~= hkl409 then   -- если текущая раскладка не рус.
                ffi.C.SendMessageA(ffi.C.GetForegroundWindow(), WM_INPUTLANGCHANGEREQUEST, INPUTLANGCHANGE_SYSCHARSET, ffi.cast('LPARAM', hkl409))
                CurrentLayout = hkl409
            end
	    vk = ffi.C.VkKeyScanExA(symbol:byte(), hkl409)
        end

        if bit.band(vk, 256) == 256 then
            if  symbol:byte() > 191 or symbol:byte() == 184 or symbol:byte() == 168 then
				if vk - 256 == 188 then command ('2<') -- Б
				elseif vk - 256 == 190 then command ('2>') -- Ю
				elseif vk - 256 == 219 then command ('2{') -- Х
				elseif vk - 256 == 221 then command ('2}') -- Ъ
				elseif vk - 256 == 186 then command ('2:') -- Ж
				elseif vk - 256 == 222 then command ('2"') -- Э
				elseif vk - 256 == 192 then command ('2~') -- Ё
				else
					command ('2' .. string.char(vk-256))
				end
            else
                command ('3' .. tostring(export_array.left_shift))
                command ('2' .. tostring(symbol))
                command ('4' .. tostring(export_array.left_shift))
            end
        else
            if  symbol:byte() > 191 or symbol:byte() == 184 or symbol:byte() == 168 then
				if vk == 188 then command ('2,') -- б
				elseif vk == 190 then command ('2.') -- ю
				elseif vk == 219 then command ('2[') -- х
				elseif vk == 221 then command ('2]') -- ъ
				elseif vk == 186 then command ('2;') -- ж
				elseif vk == 222 then command ("2'") -- э
				elseif vk == 192 then command ('2`') -- ё
				else
					command ('2' .. string.char(vk+32))
				end
            else
				command ('2' .. tostring(symbol))
            end
        end
    end

    if CurrentLayout ~= Layout then   -- вернуть раскладку, ту что была до вызова функции
        ffi.C.SendMessageA(ffi.C.GetForegroundWindow(), WM_INPUTLANGCHANGEREQUEST, INPUTLANGCHANGE_SYSCHARSET, ffi.cast('LPARAM', Layout))
    end
end


export_array.key_down = function (code)
     if type(code) == 'number' then command ('3' .. tostring(tonumber(code)))
     else command ('3' .. tostring(code:byte()))
     end
end

export_array.key_up = function (code)
     if type(code) == 'number' then command ('4' .. tostring(tonumber(code)))
     else command ('4' .. tostring(code:byte()))
     end
end



export_array.mouse = {}


export_array.mouse.move = function (x, y)
    local mouseX, mouseY = mouse_pos('abs')
    local znakX, znakY = '+', '+'
    if mouseX - x > 0 then znakX = '-' end
    if mouseY - y > 0 then znakY = '-' end
    command ('5' .. znakX .. znakY .. tostring(math.abs(mouseX - x) * 0xFFFF + math.abs(mouseY - y)))
end


export_array.mouse.click = function (x, y, button)
    if button == nil then button = export_array.mouse_left_button end
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('6' .. tostring(button))
end

export_array.mouse.left = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('6' .. tostring(export_array.mouse_left_button))
end

export_array.mouse.right = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('6' .. tostring(export_array.mouse_right_button))
end

export_array.mouse.middle = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('6' .. tostring(export_array.mouse_middle_button))
end



export_array.mouse.dbl = function (x, y, button)
    if button == nil then button = export_array.mouse_left_button end
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('6' .. tostring(button))
    command ('6' .. tostring(button))
end

export_array.mouse.left_dbl = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('6' .. tostring(export_array.mouse_left_button))
    command ('6' .. tostring(export_array.mouse_left_button))
end

export_array.mouse.right_dbl = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('6' .. tostring(export_array.mouse_right_button))
    command ('6' .. tostring(export_array.mouse_right_button))
end

export_array.mouse.middle_dbl = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('6' .. tostring(export_array.mouse_middle_button))
    command ('6' .. tostring(export_array.mouse_middle_button))
end



export_array.mouse.down = function (x, y, button)
    if button == nil then button = export_array.mouse_left_button end
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('7' .. tostring(button))
end

export_array.mouse.left_down = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('7' .. tostring(export_array.mouse_left_button))
end

export_array.mouse.right_down = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('7' .. tostring(export_array.mouse_right_button))
end

export_array.mouse.middle_down = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('7' .. tostring(export_array.mouse_middle_button))
end

export_array.mouse.up = function (x, y, button)
    if button == nil then button = export_array.mouse_left_button end
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('8' .. tostring(button))
end

export_array.mouse.left_up = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('8' .. tostring(export_array.mouse_left_button))
end

export_array.mouse.right_up = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('8' .. tostring(export_array.mouse_right_button))
end

export_array.mouse.middle_up = function (x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('8' .. tostring(export_array.mouse_middle_button))
end

export_array.mouse.drag = function (x, y, x2, y2)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    export_array.mouse.left_down(x, y)
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x2, y2)
    end
    export_array.mouse.left_up(x2, y2)
end

export_array.mouse.wheel_up = function (x, y, wheel)
    if wheel == nil then wheel = 1 end
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('9' .. tostring(math.abs(wheel)))
end

export_array.mouse.wheel_down = function (x, y, wheel)
    if wheel == nil then wheel = -1 end
    if x ~= nil and y ~= nil then
        export_array.mouse.move(x, y)
    end
    command ('9' .. tostring(-math.abs(wheel)))
end

export_array.get_port = function (vid, pid)
    if vid == nil then return -1 end
    if pid == nil then return -2 end

    local com = 0
    local DeviceInfoSet = ffi.new('HDEVINFO')
    local DeviceIndex = 0
    local DeviceInfoData = ffi.new('SP_DEVINFO_DATA', 0)
    local DevEnum = ffi.new('PCSTR', "USB")
    local ExpectedDeviceId = 'VID_' .. tostring(vid) .. '&PID_' .. tostring(pid)
    local szBuffer = ffi.new('unsigned char[1024]', 0)
    local ulPropertyType = ffi.new('DEVPROPTYPE[1]')
    local dwSize = ffi.new('PDWORD')
    DeviceInfoSet = setupapi.SetupDiGetClassDevsA(nil, DevEnum, nil, bit.bor(DIGCF_ALLCLASSES, DIGCF_PRESENT))
    DeviceInfoData.cbSize = ffi.sizeof(DeviceInfoData)

    while setupapi.SetupDiEnumDeviceInfo(DeviceInfoSet, DeviceIndex, DeviceInfoData) do
        DeviceIndex = DeviceIndex + 1
        if (setupapi.SetupDiGetDeviceRegistryPropertyA(DeviceInfoSet, DeviceInfoData, SPDRP_HARDWAREID, ulPropertyType, szBuffer, ffi.sizeof(szBuffer), dwSize)) then
            if ffi.string(szBuffer):match(ExpectedDeviceId) then
                local hDeviceRegistryKey = ffi.new('HKEY')
                hDeviceRegistryKey = setupapi.SetupDiOpenDevRegKey(DeviceInfoSet, DeviceInfoData, DICS_FLAG_GLOBAL, 0, DIREG_DEV, KEY_READ);
                local pszPortName = ffi.new('char[?]', BUFF_LEN)
                local dwSize = ffi.new('DWORD[1]', ffi.sizeof(pszPortName))
                local dwType = ffi.new('DWORD[1]')
                if advapi32.RegQueryValueExA(hDeviceRegistryKey, "PortName", nil, dwType, pszPortName, dwSize) == ERROR_SUCCESS and dwType[0] == REG_SZ then
                    com = tonumber(ffi.string(pszPortName):match('%d+'))
                end
            end
            advapi32.RegCloseKey(hDeviceRegistryKey)
        end
    end
    setupapi.SetupDiDestroyDeviceInfoList(DeviceInfoSet)
    return com
end

return export_array